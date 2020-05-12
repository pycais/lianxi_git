import json

import os
from flask import Blueprint, abort, request, session, jsonify, render_template, g
from flask_mail import Message
from flask_sqlalchemy import Pagination

from myapp import settings
from myapp.models import *
from myapp.ext import db, cache, mail

blog = Blueprint("blog", __name__)

def init_blog_blueprint(app):
    app.register_blueprint(blog)

@blog.route("/edit_blog")
def edit_blog_view():
    # 查询所有的tag
    tags = Tag.query.all()
    return render_template("blog/edit_blog.html", tags=tags)

@blog.route("/blog", methods=["GET", "POST"])
def blog_api():
    if request.method == "GET":
        # 查询一个博文 返回详情页
        blog_id = request.args.get("id")
        blog = Blog.query.get_or_404(blog_id)
        user_id = g.user.id if g.user else 0
        # 记录浏览信息
        visited = Visited(user_id=user_id, blog_id=int(blog_id))
        db.session.add(visited)
        db.session.commit()
        comments = []
        # for i in blog.comments:
        #     tmp = {
        #         "comment_time": str(i.comment_time),
        #         "content": i.content,
        #         "user_name": i.user.name
        #     }
        #     comments.append(tmp)
        # print(sorted(comments, lambda dic:dic['comment_time'], reverse=True))
        blog.comments = sorted(blog.comments, key=lambda x:x.comment_time, reverse=True)
        # 返回单个博客的详情
        return render_template("blog/blog.html", blog=blog)
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
        # 单个追加
        # blog.append(单个tag对象)
        # 移除
        # blog.remove(单个tag对象)
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

# @blog.route("/tags_blog")
# def blogs_view():
#     tag = Tag.query.get(1)
#     for i in tag.blogs:
#         print(i.title)
#     return "OK"

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

@blog.route("/blogs")
# @cache.cached(timeout=10)
def blogs_view():
#     知道tag的id
    print(request.path, "视图函数")
    print(g.user)
    tag_id = request.args.get("tag_id", 1)
#     查tag数据
    tag = Tag.query.get_or_404(tag_id)
    tags = Tag.query.all()
    # blogs = tag.blogs
    # 查询博客的标签包含了我们tag id的数据(contains可以帮我们做)
    paginations = Blog.query.filter(
        Blog.tags.contains(tag)
    ).order_by("-create_time").paginate(per_page=settings.PER_PAGE)
    data = {
        'pagination':paginations,
        'tag_id':int(tag_id),
        'titles':tags,
        'is_login': g.user is not None
    }
    return render_template("blog/blogs.html", **data)

@blog.before_request
def before_req_proccess():
    uid = session.get("user_id")
    if uid:
        g.user = User.query.get(int(uid))
    else:
        g.user = None
    # print(request.path)
    # print(request.remote_addr)


@blog.route("/blog/comment", methods=["POST"])
def blog_comment_api():
    user = g.user
    if not user or not isinstance(user, User):
        res = {
            "code": 1,
            "msg": "您未登录,请先登录",
            "data":{
                "next": "/login"
            }
        }
        return jsonify(res)
    params = request.form
    blog_id = int(params.get("blog_id"))
    content = params.get("content")
#     创建数据
    comment = Comment(
        user_id=user.id,
        blog_id=blog_id,
        content=content
    )
    db.session.add(comment)
    db.session.commit()
    # 返回结果
    res = {
        "code": 0,
        "msg": "评论成功",
        "data": {
            "next":"/blog?id=%d" % blog_id
        }
    }
    return jsonify(res)
# @blog.app_template_filter
# def upper_filter(s):
#     print(s, "--------")
#     return s.upper()

# @blog.context_processor
# def context():
#     return {"hehe": "呵呵"}

# @blog.errorhandler(500)
# def proccess_exeptions(exption):
#     # 发送错误邮件了
#     env = os.environ.get("DEBUG", True)
#     print("哈哈哈", exption)
#     if env:
#         recipients = [admin[1] for admin in settings.ADMINS]
#         print(recipients)
#         config = settings.config.get("debug")
#         msg = Message(
#             "python论坛BUG",
#             recipients,
#             body=str(exption),
#             sender=config.MAIL_DEFAULT_SENDER
#         )
#         mail.send(msg)
#
#     return "程序猿正在抓紧维修BUG"

