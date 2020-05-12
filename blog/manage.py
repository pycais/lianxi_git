from myapp import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

app = create_app("debug")
manager = Manager(app)
# 添加migrate命令
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
