from flask import Flask
from myapp.ext import init_ext
from .views import init_blue
from myapp.settings import config

def create_app(env="debug"):
    app = Flask("myapp")
    app.config.from_object(config[env])
    # 注册第三方插件
    init_ext(app)
    # 注册蓝图
    init_blue(app)
    # app.register_blueprint(blue)
    # 配置
    # app.config["SECRET_KEY"] = "snjkdbfhsd289uysdfhi"
    # app.config["SESSION_TYPE"] = "redis"
    # app.config["SESSION_COOKIE_NAME"] = "duita"
    # app.config["SESSION_KEY_PREFIX"] = "o_o:"
    # app.config["SESSION_REDIS"] = redis.Redis(host="sharemsg.cn",db=10) #session在Redis的存储位置
    # # 数据库的配置
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:liuda6015?@127.0.0.1:3306/fl01"
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # 实例化第三方插件
    # se = Session()
    # se.init_app(app)
    # # sqlalchemy的绑定APP
    # db.init_app(app)
    # # 实例化migrate
    # migrate.init_app(app=app, db=db)
    return app