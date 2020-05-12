import json

from flask import Blueprint, request, session, jsonify
from myapp.models import *
from myapp.ext import db

blog = Blueprint("blog", __name__)

def init_blog_blueprint(app):
    app.register_blueprint(blog)

@blog.route("/blog", methods=["GET", "POST"])
def blog_api():
    if request.method == "GET":
        pass
        # 返回单个博客的详情
    else:
        params = request.form
        uid = session.get("user_id")
        tags = json.loads(params.get("tags"))

        if not uid:
            res = {
                "code": 0,
                "data": "",
                "msg": "请先登录"
            }
            return jsonify(res)

        blog = Blog(
                title=params.get("title"),
                content=params.get("content"),
                author_id=int(uid)
            )
        db.session.add(blog)
        db.session.commit()
        # 处理tags
        tags = [Tag.query.get(int(i)) for i in tags]
        blog.tags = tags
        db.session.add(blog)
        db.session.commit()
        res = {
            "code": 0,
            "msg": "创建成功"
        }
        return jsonify(res)

# 多对多关系查询
@blog.route("/blog_tags")
def tags_view():
    blog = Blog.query.get(3)
    for i in blog.tags:
        print(i.name)
    return "OK"

@blog.route("/tags_blog")
def blogs_view():
    tag = Tag.query.get(1)
    for i in tag.blogs:
        print(i.title)
    return "OK"

@blog.route("/blog/user")
def user_blog():
    blog = Blog.query.get(3)
    return blog.author.name

@blog.route("/user/blogs")
def user_blogs():
    uid = session.get("user_id")
    user = User.query.get(int(uid))
    for i in user.blogs:
        print(i.title)
    return "OK"


