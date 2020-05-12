from flask import Flask
from myapp.ext import init_ext
from myapp.settings import config
from myapp.views.blog_view import init_blog_blueprint
from myapp.views.index_view import init_blueprint
from myapp.views.user_view import init_user_blueprint


def create_app(env="debug"):
    app = Flask("myapp")
    # 配置
    app.config.from_object(config.get(env))
    # 实例化第三方的插件
    init_ext(app)
    # 初始化蓝图
    init_blueprint(app)
    init_user_blueprint(app)
    init_blog_blueprint(app)
    return app