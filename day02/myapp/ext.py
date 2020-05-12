from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()
def init_ext(app):
    se = Session()
    se.init_app(app)
    # sqlalchemy的绑定APP
    db.init_app(app)
    # 实例化migrate
    migrate.init_app(app=app, db=db)