from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('mysql+pymysql://username:password@ip/test')
Session = sessionmaker(bind=engine)
session = Session()


class ModelMerger:
    def __init__(self):
        self.merged_model = {}

    def parse_value(self, value):
        """
        解析单个值，返回其类型描述。
        """
        if isinstance(value, dict):
            return self.parse_dict(value)
        elif isinstance(value, list):
            if value:
                return [self.parse_value(value[0])]
            else:
                return ['Any']
        elif isinstance(value, str):
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
        """
        递归解析字典，生成每个键值对的类型描述。
        """
        parsed = {}
        for key, value in d.items():
            parsed[key] = self.parse_value(value)
        return parsed

    def merge_values(self, v1, v2):
        """
        合并两个值，可以是类型、列表或字典，处理空列表和非空列表的合并。
        """
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
            if 'Any' in (v1, v2) and v1 != v2:
                return [t for t in (v1, v2) if t != 'Any'][0]
            return v1 if v1 == v2 else 'Any'

    def merge_dicts(self, d1, d2):
        """
        合并两个已解析的字典，处理类型冲突。
        """
        for key, value in d2.items():
            if key in d1:
                d1[key] = self.merge_values(d1[key], value)
            else:
                d1[key] = value
        return d1

    def add_dict(self, new_dict):
        """
        添加新字典并更新合并后的模型。
        """
        parsed_dict = self.parse_dict(new_dict)
        self.merged_model = self.merge_dicts(self.merged_model, parsed_dict)

    def get_model(self):
        """
        获取当前合并后的模型。
        """
        return self.merged_model


def create_sqlalchemy_model(table_name, model_description, base_class, relationships=None):
    """
    Generate a SQLAlchemy model class from a model description.
    根据模型描述生成 SQLAlchemy 模型类，添加主键 id，并处理嵌套关系的主键和外键。
    """
    attributes = {'__tablename__': table_name}
    relationships = relationships or {}

    # Add a primary key 'id' to every table
    attributes['id'] = Column(Integer, primary_key=True)
    # Add a create_time field to every table
    attributes['create_time'] = Column(DateTime, default=datetime.utcnow)

    for key, value in model_description.items():
        if isinstance(value, str):
            if value == 'str':
                attributes[key] = Column(String(64))
            elif value == 'int':
                attributes[key] = Column(Integer)
            elif value == 'float':
                attributes[key] = Column(Float)
            elif value == 'bool':
                attributes[key] = Column(Boolean)
            else:
                attributes[key] = Column(String)
        elif isinstance(value, list) and value:
            nested_table_name = f"{table_name}_{key}"
            nested_model_class = create_sqlalchemy_model(nested_table_name, value[0], base_class)
            attributes[f"{key}_id"] = Column(Integer, ForeignKey(f"{nested_table_name}.id"))
            attributes[key] = relationship(nested_model_class, backref=table_name)
        elif isinstance(value, dict):
            nested_table_name = f"{table_name}_{key}"
            nested_model_class = create_sqlalchemy_model(nested_table_name, value, base_class)
            attributes[f"{key}_id"] = Column(Integer, ForeignKey(f"{nested_table_name}.id"))
            attributes[key] = relationship(nested_model_class, backref=table_name)

    return type(table_name.capitalize(), (base_class,), attributes)


# Example usage
model_merger = ModelMerger()

input_data1 = {
    "name": "Alice",
    "age": 30,
    "address": []
}

input_data2 = {
    "name": "Bob",
    "age": 25,
    "address": [
        {"addr": "123 Main St", "num": 231, "ee": '123'},
        {"addr": "123 Main St2", "num": 21}
    ]
}

input_data3 = {
    "name": "Bob",
    "age": 25,
    "address": [
        {"addr": "123 Main St2", "num": 21, 'xx': 123}
    ]
}

# Adding dictionaries one by one
model_merger.add_dict(input_data1)
model_merger.add_dict(input_data3)
model_merger.add_dict(input_data2)

# Getting the merged model
merged_model = model_merger.get_model()
print(merged_model)

# Creating SQLAlchemy models
MainModel = create_sqlalchemy_model('main', merged_model, Base)
Base.metadata.create_all(engine)

# Example of adding data to the created tables
new_record = MainModel(name="Charlie", age=28)
session.add(new_record)
session.commit()
