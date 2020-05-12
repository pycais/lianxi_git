import os
import random
from PIL import Image, ImageFont, ImageDraw
from flask import abort, jsonify, redirect
from io import BytesIO

from flask import Blueprint, render_template, request, session, make_response

from myapp import settings
from myapp.ext import db
from myapp.models import *
from myapp.util import get_random_color, enc_pwd

user = Blueprint("user", __name__)

def init_user_blueprint(app):
    app.register_blueprint(user)

@user.route("/register", methods=["GET", "POST"])
def register_view():
    if request.method == "GET":
        return render_template("/user/register.html")
    elif request.method == "POST":
    #     注册逻辑
        params = request.form
        name = params.get("name")
        pwd = params.get("pwd")
        confirm_pwd = params.get("confirm_pwd")
        email = params.get("email")
        verify = params.get("verify")
        server_verify = session.get("code")
        # 判断验证码
        if verify.upper() != server_verify.upper():
            res = {
                "code": 1,
                "msg": "验证码不正确"
            }
            return jsonify(res)
    #     做校验
        if not name or not pwd or not confirm_pwd or not email:
            res = {
                "code":1, 
                "msg": "信息不完整"
            }
            return jsonify(res)
        user = User.query.filter_by(name=name).first()
        if pwd != confirm_pwd:
            res = {
                "code": 1,
                "msg": "密码和确认密码不一致"
            }
            return jsonify(res)
        if not user:
            # 创建用户
            user_data = User(
                name=name,
                password=enc_pwd(pwd),
                email=email
            )
            db.session.add(user_data)
            db.session.commit()
            res = {
                "code":0,
                "msg": "OK",
                "data":{
                    "next": "/login"
                }
            }
            return jsonify(res)
        else:
            res = {
                "code": 1,
                "msg": "该用户已存在"
            }
            return jsonify(res)
    else:
        abort(405)

@user.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "GET":
        return render_template("user/login.html")
    else:
    #         解析参数
        params = request.form
        name = params.get("name")
        pwd = params.get("pwd")
        verify = params.get("verify")
        server_verify = session.get("code")
    # 校验数据
        if verify.upper() != server_verify.upper():
            res = {
                "code": 1,
                "msg": "验证码不正确"
            }
            return jsonify(res)

        if not name or not pwd:
            res = {
                "code": 1,
                "msg": "信息不完整"
            }
            return jsonify(res)

        # 校验用户
        #     找人
        user = User.query.filter(User.name.__eq__(name)).first()
        # 判断密码 以及是否活跃
        if user and user.is_active and user.password == enc_pwd(pwd):
            res = {
                "code": 0,
                "msg": "OK",
                "data": {
                    "next": "/"
                }
            }
            # 如果成功就登录
            session["user_id"] = user.id
            response = jsonify(res)
            return response
        else:
            res = {
                "code": 1,
                "msg": "账号或密码错误"
            }
            return jsonify(res)

@user.route("/captcha/<rand>")
def verify_img(rand):
    # 实例化一个画布
    img_size = (200, 50)
    bg_color = get_random_color()
    img = Image.new("RGB", img_size, bg_color)

    # 实例化字体
    font_path = os.path.join(
        settings.BASE_DIR, "myapp/static/fonts/ADOBEARABIC-BOLDITALIC.OTF"
    )
    font_size = 40
    font = ImageFont.truetype(font_path, font_size)
    # 实例化一个画笔
    draw = ImageDraw.Draw(img)
    # 准备数据源
    source = "zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP1234567890"
    # my_str = random.choice(source, 4)
    my_str = random.sample(source, 4)
    index = 0
    for i in my_str:
        draw.text((30+(font_size*index), 5), i, fill=get_random_color(), font=font)
        index += 1

    for i in range(1000):
        x = random.randint(0, 200)
        y = random.randint(0, 70)
        draw.point((x,y), get_random_color())
    # 实例化缓存区
    buf = BytesIO()
    img.save(buf, "png")
    session["code"] = "".join(my_str)
    response = make_response(buf.getvalue())
    response.headers["Content-Type"] = "image/png"
    return response

@user.route("/logout")
def logout_view():
    session.pop("user_id")
    return redirect("/")

