import os
import redis

def get_db_uri(db_config):
    uri = "{backend}+{engine}://{user}:{password}@{host}:{port}/{db}".format(
        **db_config
    )
    return uri

class Config:
    debug = False
    test = False
    online = False
    SECRET_KEY = "snjkdbfhsd289uysdfhi"
    SESSION_TYPE = "redis"
    SESSION_COOKIE_NAME = "dada"
    SESSION_KEY_PREFIX = "myapp_session:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DebugConfig(Config):
    debug = True
    SESSION_REDIS = redis.Redis(host="sharemsg.cn",db=10)
    DATABASE = {
        "backend": "mysql",
        "engine": "pymysql",
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "liuda6015?",
        "db": "pythonblog"
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class TestConfig(Config):
    debug = True
    SESSION_REDIS = redis.Redis(host="sharemsg.cn",db=11)
    DATABASE = {
        "backend": "mysql",
        "engine": "pymysql",
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "liuda6015?",
        "db": "fl01_test"
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)

config = {
    "debug": DebugConfig,
    "test": TestConfig
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
