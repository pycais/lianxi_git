import math
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('mysql+pymysql://username:password@ip:3306/database')
Session = sessionmaker(bind=engine)


class ModelMerger:
    def __init__(self):
        self.merged_model = {}
        self.string_lengths = {}

    def parse_value(self, key, value):
        """Helper function to parse a value and return its type as a string."""
        if isinstance(value, dict):
            return self.parse_dict(value)
        elif isinstance(value, list):
            if value:
                return [self.parse_value(key, value[0])]
            else:
                return ['Any']
        elif isinstance(value, str):
            length = len(value)
            if key in self.string_lengths:
                self.string_lengths[key] = max(self.string_lengths[key], length)
            else:
                self.string_lengths[key] = length
            return 'str'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, bool):
            return 'bool'
        else:
            return 'Any'

    def parse_dict(self, d):
        """Helper function to parse a dictionary and return its type as a dictionary."""
        parsed = {}
        for key, value in d.items():
            parsed[key] = self.parse_value(key, value)
        return parsed

    def merge_values(self, v1, v2):
        """Merge two values which could be types, lists or dictionaries."""
        if isinstance(v1, dict) and isinstance(v2, dict):
            return self.merge_dicts(v1, v2)
        elif isinstance(v1, list) and isinstance(v2, list):
            if v1 and v2:
                return [self.merge_values(v1[0], v2[0])]
            elif not v1:
                return v2
            else:
                return v1
        else:
            if v1 == 'Any':
                return v2
            elif v2 == 'Any':
                return v1
            if v1 != v2:
                return 'Any'
            return v1

    def merge_dicts(self, d1, d2):
        """Merge two parsed dictionaries."""
        for key, value in d2.items():
            if key in d1:
                d1[key] = self.merge_values(d1[key], value)
            else:
                d1[key] = value
        return d1

    def add_dict(self, new_dict):
        """Add a new dictionary to the model and merge its structure."""
        parsed_dict = self.parse_dict(new_dict)
        self.merged_model = self.merge_dicts(self.merged_model, parsed_dict)

    def get_model(self):
        """Get the current merged model."""
        return self.merged_model


class TableCreator:
    def __init__(self, engine, base, main_identifier='name', main_identifier_type='str', main_table_name='main'):
        self.engine = engine
        self.base = base
        self.main_identifier = main_identifier
        self.models_dict = {}
        self.session = Session()
        self.main_identifier_type = main_identifier_type
        self.main_table_name = main_table_name

    def next_power_of_2(self, x):
        """Calculate the next power of 2 greater than or equal to x."""
        return 2 ** math.ceil(math.log2(x))

    def get_sqlalchemy_type(self, value, key, string_lengths):
        """Return the appropriate SQLAlchemy column type based on the value."""
        if value == 'str':
            max_length = string_lengths.get(key, 64)
            adjusted_length = self.next_power_of_2(max_length)
            return String(adjusted_length)
        elif value == 'int':
            return Integer
        elif value == 'float':
            return Float
        elif value == 'bool':
            return Boolean
        else:
            return String(64)  # Default type

    def create_sqlalchemy_model(self, table_name, model_description, string_lengths):
        """Generate a SQLAlchemy model class from a model description."""
        attributes = {'__tablename__': table_name}

        # Add a primary key 'id' to every table
        attributes['id'] = Column(Integer, primary_key=True)

        # Add a create_time field to every table
        attributes['create_time'] = Column(DateTime, default=datetime.utcnow)

        # 作为表关联的标识，以下创建二选其一，不可同时选择
        flag = table_name == self.main_table_name
        # Add the logical relationship field, 指定一个在字典中的键作为列
        attributes[self.main_identifier] = Column(
            self.get_sqlalchemy_type(self.main_identifier_type, self.main_identifier, string_lengths),
            unique=flag, index=True)

        # Add the logical relationship field, 指定一个不在字典中的键作为列，自主定义的字段
        # attributes[self.main_identifier] = Column(
        #     self.get_sqlalchemy_type('str', self.main_identifier, string_lengths), unique=flag, index=True)

        for key, value in model_description.items():
            if isinstance(value, str):
                if key == self.main_identifier:
                    continue
                attributes[key] = Column(self.get_sqlalchemy_type(value, key, string_lengths))
            elif isinstance(value, list) and value:
                nested_table_name = f"{table_name}_{key}"
                nested_model_class = self.create_sqlalchemy_model(nested_table_name, value[0], string_lengths)
                self.models_dict[nested_table_name] = nested_model_class
            elif isinstance(value, dict):
                nested_table_name = f"{table_name}_{key}"
                nested_model_class = self.create_sqlalchemy_model(nested_table_name, value, string_lengths)
                self.models_dict[nested_table_name] = nested_model_class

        model_class = type(table_name.capitalize(), (self.base,), attributes)
        self.models_dict[table_name] = model_class
        print(attributes, flag, table_name)
        return model_class

    def create_tables(self, model_description, string_lengths):
        """Create all tables based on the model description."""
        main_model = self.create_sqlalchemy_model(self.main_table_name, model_description, string_lengths)
        self.base.metadata.create_all(self.engine)
        return main_model

    def insert_data(self, model_class, data, main_id_value):
        """Insert data into the corresponding SQLAlchemy model class."""
        if isinstance(data, list):
            for item in data:
                self.insert_data(model_class, item, main_id_value)
            return

        if not isinstance(data, dict):
            return

        instance_data = {self.main_identifier: main_id_value}
        relationships_data = {}

        for key, value in data.items():
            if isinstance(value, list) or isinstance(value, dict):
                relationships_data[key] = value
            else:
                instance_data[key] = value

        instance = model_class(**instance_data)
        self.session.add(instance)
        self.session.flush()  # Ensure the instance gets an ID before inserting related data

        for key, value in relationships_data.items():
            related_table_name = f"{model_class.__tablename__}_{key}"
            related_model = self.models_dict[related_table_name]
            related_data = value

            if isinstance(related_data, list):
                for item in related_data:
                    item[self.main_identifier] = main_id_value
            elif isinstance(related_data, dict):
                related_data[self.main_identifier] = main_id_value

            self.insert_data(related_model, related_data, main_id_value)

        self.session.commit()

    def add_data(self, main_model, data_list):
        """Add multiple dictionaries to the created tables."""
        for data in data_list:
            main_id_value = data[self.main_identifier]
            self.insert_data(main_model, data, main_id_value)


if __name__ == '__main__':
    # Example usage
    model_merger = ModelMerger()
    import secrets

    input_data1 = {
        "name": "d{}".format(secrets.randbelow(1000000)),
        "age": secrets.randbelow(1000000),
        "address": []
    }

    input_data2 = {
        "name": "d{}".format(secrets.randbelow(1000000)),
        "age": secrets.randbelow(1000000),
        "address": [
            {"addr": "123 Main St", "num": 231, "ee": '123'},
            {"addr": "123 Main St2", "num": 21}
        ]
    }

    input_data3 = {
        "name": "d{}".format(secrets.randbelow(1000000)),
        "age": secrets.randbelow(1000000),
        "address": [
            {"addr": "123 Main St2", "num": 2211, 'xx': 123},
            {"addr": "123 Main St2", "num": 2212, 'xx': 32},
            {"addr": "123 Main St2", "num": 2213, 'ee': 'ad'}
        ]
    }

    # Adding dictionaries one by one
    model_merger.add_dict(input_data1)
    model_merger.add_dict(input_data2)
    model_merger.add_dict(input_data3)

    # Getting the merged model
    merged_model = model_merger.get_model()
    print(merged_model)
    print(model_merger.string_lengths)
    # Creating tables and inserting data
    main_identifier = 'age'  # 创建表时关联字段，该字段是字典中的字段，主表字段
    table_creator = TableCreator(engine, Base, main_identifier=main_identifier, main_table_name='main3',
                                 main_identifier_type=merged_model[main_identifier])
    main_model = table_creator.create_tables(merged_model, model_merger.string_lengths)
    table_creator.add_data(main_model, [input_data1, input_data2, input_data3])

    # Query the database to verify data insertion
    session = Session()
    for instance in session.query(main_model).all():
        print(instance.name, instance.age)
