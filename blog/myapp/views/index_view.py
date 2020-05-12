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
    if uid:
        is_login = True
    return render_template("index/index.html", is_login=is_login)
