from flask import Flask, session
import logging
from logging.handlers import RotatingFileHandler
from flask_admin import Admin
from flask_babelex import Babel
from flask_principal import Permission, Principal, RoleNeed, identity_loaded, UserNeed
from flask_login import LoginManager
from datetime import timedelta

app = Flask(__name__, instance_relative_config=True)
# 加载配置
app.config.from_object('config')
app.config.from_pyfile('config.py')

# 加载,添加admin权限
principals = Principal()
admin_permission = Permission(RoleNeed('admin'))

# 初始化login_manager
login_manager = LoginManager()
login_manager.login_message = '请登录'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'
login_manager.login_view = 'unlogin'
login_manager.init_app(app)

# #设置session和cookie类型
# session.permanent = True
# app.permanent_session_lifetime = timedelta(minutes=10)
# login_manager.remember_cookie_duration = timedelta(days=1)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# 初始化后台管理
admin = Admin(app, name='后台管理')

# 配置国际化语言
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

# 记录日志
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.WARNING)
app.logger.addHandler(handler)

#  路由
from .routes import *

#  REST API  接口路由
from .restapi import *

#  后台路由
from .admin import *
