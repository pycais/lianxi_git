from flask import Flask

from myapp.models import db
from myapp.views import blue



def create_app():
    app = Flask(__name__)
    # 配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://qiaofeng:1025@150.158.123.234:3306/fl01'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(blue)
    return app