from . import admin, app, login_manager, login
from flask_admin import BaseView, expose, Admin
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from .model import *
from flask_admin.contrib.fileadmin import FileAdmin
from flask_security import current_user
from .model.user import User



class MyView(BaseView):
    # 对应键
    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role('Admin'):
            return True
        return False
    @expose('/')
    def index(self):
        url = url_for('.index')
        return self.render('admin/select.html', url=url)


class Create(BaseView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role('Admin'):
            return True
        return False
    @expose('/')
    def create(self):
        url = url_for('.create')
        return self.render('admin/create.html', url=url)


class Model_User_MyView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role('Admin'):
            return True
        return False
    can_create = False
    column_labels = {
        'username': '用户名',
        'password': '密码',
        'phone': '联系方式',
        'email': '电子邮箱',
        'id': '用户ID'
    }
    column_list = ('username', 'password', 'phone', 'email', 'id')

    def __init__(self, session, **kwargs):
        super(Model_User_MyView, self).__init__(User, session, **kwargs)


admin.add_view(MyView(name='Hello 1', endpoint='test1', category='下拉框'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='下拉框'))
admin.add_view(MyView(name='Hello 3', endpoint='test3', category='下拉框'))

admin.add_view(Model_User_MyView(db.session, name='用户管理'))
admin.add_view(Create(name='创建用户'))
