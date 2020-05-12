from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
db = SQLAlchemy()
migrate = Migrate()
se = Session()

def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    se.init_app(app)