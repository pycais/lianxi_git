from flask_script import Manager
from myapp import create_app
from flask_migrate import MigrateCommand

app = create_app("debug")
manager = Manager(app)
# 添加db的命令
manager.add_command("db", MigrateCommand)
if __name__ == '__main__':
    manager.run()
