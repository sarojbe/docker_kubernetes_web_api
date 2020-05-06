from todolist import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask import current_app


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

class User(db.Model):
    username= db.Column(db.String(20),unique=True, nullable=False)
    email= db.Column(db.String(40) ,unique=True, nullable=False)
    password= db.Column(db.String(60) , nullable=False)

class Entry(db.Model):
    username= db.Column(db.String(20),unique=True, nullable=False)
    what_to_do= db.Column(db.String(40) ,unique=True, nullable=False)
    due_date= db.Column(db.String(60) , nullable=False)