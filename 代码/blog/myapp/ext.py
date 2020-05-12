from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
db = SQLAlchemy()
migrate = Migrate()
se = Session()
cache = Cache(config={
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_URL":"redis://127.0.0.1:6379/3",
    "CACHE_DEFAULT_TIMEOUT": 20
})
toolbar = DebugToolbarExtension()
mail = Mail()
def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    se.init_app(app)
    cache.init_app(app)
    toolbar.init_app(app)
    mail.init_app(app)