from flask import Blueprint, jsonify
from myapp.models import db, User

blue = Blueprint("myapp", __name__)


@blue.route('/')
def index():
    return 'hello'


@blue.route('/create_all')
def create_all():
    db.create_all()
    print('--' * 100)
    return 'OK'


@blue.route('/drop_all')
def drop_all():
    db.drop_all()
    return 'odko'


@blue.route('/add_data')
def add_data():
    user = []
    for i in range(10):
        user.append(User(movie_path=f'aaa{i}', is_active=False))
    db.session.add_all(user)
    db.session.commit()
    return '保存'


@blue.route('/get_data')
def get_data():
    user = User.query.all()
    print(user)
    return jsonify({'wd': 2})

@blue.route('/index/<id:int>')