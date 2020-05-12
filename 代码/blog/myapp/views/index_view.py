from flask import Blueprint, render_template, session
from myapp.ext import db
from myapp.models import *

blue = Blueprint("myapp", __name__, static_folder="static", template_folder="templates")

def init_blueprint(app):
    app.register_blueprint(blue)



@blue.route("/")
def index_view():
    is_login = False
    # 看session
    uid = session.get("user_id")
    tags = Tag.query.all()
    web_msg = WebsiteIndex.query.filter_by(is_use=True).first()
    notices = Notice.query.filter_by(is_use=True).limit(3)
    if uid:
        is_login = True
    return render_template("index/index.html", is_login=is_login, titles=tags, tag_id=0, web_msg=web_msg, notices=notices)
