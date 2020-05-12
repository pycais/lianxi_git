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


class Grade(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(30),
        nullable=False
    )
    stus = db.relationship("Stu", backref="grade", lazy=True)

class Stu(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(30),
        nullable=False
    )
    grade_id = db.Column(
        db.Integer,
        db.ForeignKey("grade.id"),
        nullable=False
    )

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('pages', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)