#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os import urandom
from hashlib import md5
from . import db
from flask_security import UserMixin
from .role_user import roles_users

class User(db.Model, UserMixin):
    # 表名
    __tablename__ = 'user'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_number = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(60))
    real_name = db.Column(db.String(60))
    t_gender = db.Column(db.String(60))
    identity_number = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    teacher = db.relationship('Teacher', uselist=False, back_populates='t_user')
    student = db.relationship('Student', uselist=False, back_populates='s_user')

    roles = db.relationship('Role', secondary=roles_users,
                                    backref=db.backref('users', lazy='dynamic'))
    #
    # def __init__(self, username, password):
    #     self.role_id = md5(username.encode('utf-8')).hexdigest()
    #     self.username = username
    #     self.salt = md5(urandom(64)).hexdigest()
    #     self.password = md5((password + self.salt).encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<id:%r 用户名:%r  密码:%r>' % (self.id, self.username, self.password)
