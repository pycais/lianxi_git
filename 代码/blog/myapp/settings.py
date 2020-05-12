import os
import redis

def get_db_uri(db_config):
    uri = "{backend}+{engine}://{user}:{password}@{host}:{port}/{db}".format(
        **db_config
    )
    return uri

class Config:
    DEBUG = False
    TEST = False
    ONLINE = False
    SECRET_KEY = "snjkdbfhsd289uysdfhi"
    SESSION_TYPE = "redis"
    SESSION_COOKIE_NAME = "dada"
    SESSION_KEY_PREFIX = "myapp_session:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "782054874@qq.com"
    MAIL_PASSWORD = "kzykkitusvhhbejc"
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DebugConfig(Config):
    DEBUG = True
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
    TEST = True
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

LOGIN_URL = "/login"

ADMINS = (
    ("dada", "cs025@163.com"),
    ("jingcheng", "409708306@qq.com"),
)
PER_PAGE = 5