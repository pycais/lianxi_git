from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    movie_path = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
        index=True
    )
    is_active = db.Column(
        db.Boolean,
        default=True
    )