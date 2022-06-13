from routes import db

from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from itsdangerous.serializer import Serializer


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(120), nullable=False)
    contact_no = db.Column(db.Integer, nullable=False)
    user_result = db.Column(db.String(200))
    score = db.Column(db.Integer)
    # posts = db.relationship('Post', backref='author', lazy=True)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     return s.dumps({'user_id': self.id})
    #
    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)


#
class Subject(db.Model):
    id = db.Column(db.Integer, unique=True, autoincrement=True)
    sub_name = db.Column(db.String(20), primary_key=True)


#
# class Topic(db.Model):
#     id = db.Column(db.Integer, autoincrement=True)
#     sub_name = db.Column(db.String(20), db.ForeignKey(Subject.sub_name), nullable=True)
#     top_name = db.Column(db.String(20), primary_key=True)
#     content = db.Column(db.String(20), unique=True, nullable=False)


#
class QA(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sub_name = db.Column(db.String(20), db.ForeignKey(Subject.sub_name), nullable=False)
    question = db.Column(db.String(100), nullable=False)
    options = db.Column(db.String(200), nullable=False)
    correct_opt = db.Column(db.String(70), nullable=False)
