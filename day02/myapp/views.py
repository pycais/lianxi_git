from flask import Blueprint, render_template, session
from myapp.models import User, Stu, Grade
from myapp.ext import db
blue = Blueprint("myapp", __name__, template_folder="templates", static_folder="static")

def init_blue(app):
    app.register_blueprint(blue)

@blue.route("/")
def index_view():
    return render_template("index/index.html")

@blue.route("/set")
def set_session():
    session["name"] = "dada"
    return "OK"

@blue.route("/get")
def get_session():
    return session.get("name")

@blue.route("/fun1")
def fun1():
    return render_template("learn/marco_one.html")

@blue.route("/filter")
def filter_view():
    data = "<h1>呵呵呵</h1>"
    return render_template("learn/filter.html", data=data)

@blue.route("/create_all")
def create_all():
    db.create_all()
    return "建好了"

@blue.route("/drop_all")
def drop_all():
    db.drop_all()
    return "删完了"

@blue.route("/create_users")
def create_users():
    users = []
    for i in range(10):
        user = User(name="张三%d" % (i+1), password="123", email="%dqqq@qq.com" % i)
        users.append(user)
        # db.session.add(user)
        # db.session.commit()
    db.session.add_all(users)
    db.session.commit()
    return "OK"

@blue.route("/get_users")
def get_users():
    # users = User.query.all()
    # users = User.query.filter(User.id.__gt__(5))
    users = User.query.filter(User.name.like("%三_"))
    return render_template("learn/users.html", users=users)

@blue.route("/grade")
def get_grade():
    stu = Stu.query.first()
    return stu.grade.name

@blue.route("/stus")
def get_stus():
    grade = Grade.query.first()
    for i in grade.stus:
        print(i.name)
    return "OK"