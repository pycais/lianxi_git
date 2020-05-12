import datetime

from myapp.ext import db

class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(30),
        nullable=False
    )
    password = db.Column(
        db.String(255)
    )
    email = db.Column(
        db.String(255),
        index=True,
        unique=True
    )
    is_active = db.Column(
        db.Boolean,
        default=True
    )
    icon = db.Column(
        db.String(255),
        nullable=True
    )
    create_time = db.Column(
        db.DateTime,
        default=datetime.datetime.now()
    )
    visiteds = db.relationship("Visited", backref="user", lazy=True)
    collects = db.relationship("Collect", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)
    blogs = db.relationship("Blog", backref="author", lazy=True)
    # 一对一关系映射
    balance = db.relationship("Balance", backref="user", lazy=True, uselist=False)

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'), primary_key=True)
)

class Blog(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column(
        db.String(100),
    )
    content = db.Column(
        db.Text()
    )
    tags = db.relationship(
        "Tag", secondary=tags,
        backref=db.backref("blogs", lazy=True),
        lazy="subquery"
    )
    create_time = db.Column(
        db.DateTime,
        default=datetime.datetime.now()
    )
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    visiteds = db.relationship("Visited", backref="blog", lazy=True)
    collects = db.relationship("Collect", backref="blog", lazy=True)
    comments = db.relationship("Comment", backref="blog", lazy=True)

class Tag(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(30)
    )

class Visited(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True
    )
    blog_id = db.Column(
        db.Integer,
        db.ForeignKey("blog.id"),
        nullable=False,
        index=True
    )
    visited_time = db.Column(
        db.DateTime,
        default=datetime.datetime.now()
    )

class Collect(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True
    )
    blog_id = db.Column(
        db.Integer,
        db.ForeignKey("blog.id"),
        nullable=False,
        index=True
    )
    collect_time = db.Column(
        db.DateTime,
        default=datetime.datetime.now()
    )

# 评论表
class Comment(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True
    )
    blog_id = db.Column(
        db.Integer,
        db.ForeignKey("blog.id"),
        nullable=False,
        index=True
    )
    content = db.Column(
        db.Text()
    )
    comment_time = db.Column(
        db.DateTime,
        default=datetime.datetime.now()
    )

# 余额
class Balance(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True
    )
    money = db.Column(
        db.Integer
    )
    update_time = db.Column(
        db.DateTime,
        default=datetime.datetime.now()
    )