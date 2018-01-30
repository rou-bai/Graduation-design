from .. import app
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
import re
from os import urandom
from flask_security import SQLAlchemyUserDatastore, Security

db = SQLAlchemy(app)

from .user import User
from .user import *
from .role_user import roles_users
from .role import Role
from .teacher import Teacher
from .student import Student
from .test import Test
from .lesson import Class
from .car import Car

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
# 初始化数据库连接
db.create_all()


# 创建管理员账号
def create_admin(admin_name, admin_password, role_name1, role_name2, role_name3, role_description1, role_description2,
                 role_description3):
    new_admin1 = User.query.filter_by(username=admin_name).first()
    if new_admin1:
        return
    else:
        new_role1 = Role.query.filter_by(name=role_name1).first()
        new_role2 = Role.query.filter_by(name=role_name2).first()
        new_role3 = Role.query.filter_by(name=role_name3).first()

        if new_role1 or new_role2 or new_role3:
            return
        else:
            salt = md5(urandom(64)).hexdigest()
            admin = user_datastore.create_user(username=admin_name, salt=salt,
                                               user_number=md5(admin_name.encode('utf-8')).hexdigest(),
                                               password=md5((admin_password + salt).encode('utf-8')).hexdigest())

            # 生成普通用户角色和admin用户角色
            student_role = user_datastore.create_role(name=role_name2, description=role_description2)
            driver_role = user_datastore.create_role(name=role_name3, description=role_description3)
            admin_role = user_datastore.create_role(name=role_name1, description=role_description1)

            # 为admin添加Admin角色
            user_datastore.add_role_to_user(admin, admin_role)
            db.session.commit()


new_user = create_admin('admin', 'admin', 'Admin', 'Student', 'Teacher', '管理员', '学员', '教练')


# 电话格式检查
def check_phone(phone):
    if phone is None:
        return None
    else:
        if len(phone) == 11:
            return phone
        else:
            return None


# 邮箱格式检查
def check_email(email):
    if email is None:
        return None
    else:
        if len(email) <= 20 and len(email) > 8:
            if re.match('^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email) != None:
                return email
            else:
                return None
        else:
            return None


# 增加学员账号
def confirm_regist(username, password, phone, email, role):
    new_salt = md5(urandom(64)).hexdigest()
    new_password = md5((password + new_salt).encode('utf-8')).hexdigest()
    new_user_number = md5(username.encode('utf-8')).hexdigest()
    user1 = user_datastore.create_user(username=username,
                                       password=new_password,
                                       user_number=new_user_number,
                                       salt=new_salt,
                                       phone=phone,
                                       email=email)
    if role == '1':
        normal_role = user_datastore.find_role('Student')
        db.session.add(user1)
        user_datastore.add_role_to_user(user1, normal_role)
        db.session.commit()
        new_student = Student(s_u_id=user1.id)
        db.session.add(new_student)
        db.session.commit()

    elif role == '2':
        normal_role = user_datastore.find_role('Teacher')
        db.session.add(user1)
        user_datastore.add_role_to_user(user1, normal_role)
        db.session.commit()
        new_student = Teacher(t_u_id=user1.id)
        db.session.add(new_student)
        db.session.commit()
    else:
        return


# 修改个人资料
def update_person_info(current_user, user, username, gender, real_name, email, phone, identity_number):
    user.user_number = md5(username.encode('utf-8')).hexdigest()
    user.username = username
    user.password = current_user.password
    user.salt = current_user.salt
    user.t_gender = gender
    user.real_name = real_name
    user.email = email
    user.phone = phone
    user.identity_number = identity_number
    db.session.add(user)
    db.session.commit()


# 修改学员部分资料
def update_student_info(current_user, student, subject):
    student.s_subject = subject
    student.s_u_id = current_user.id
    db.session.add(student)
    db.session.commit()


# 修改教练部分资料
def update_teacher_info(current_user, teacher, work_time):
    teacher.t_work_time = work_time
    teacher.t_u_id = current_user.id
    db.session.add(teacher)
    db.session.commit()


# 身份证格式检查
def check_identity_number(identity_number):
    user = User.query.filter_by(identity_number=identity_number).first()
    if user:
        return
    else:
        if len(identity_number) == 18:
            if re.match('^[0-9]{1,18}$', identity_number) != None:
                return identity_number
            else:
                return
        else:
            return


# 性别检查
def check_gender(gender):
    if gender == '男' or gender == '女':
        return gender
    else:
        return


# 真实姓名检查
def check_real_name(real_name):
    if len(real_name) <= 4:
        if re.match('^[\u4e00-\u9fa5]{2,4}$', real_name) != None:
            return real_name
        else:
            return
    else:
        return


# 学生选择教练
def student_select_teacher(teacher_id, user_id):
    student = Student.query.filter_by(s_u_id=user_id).first()
    student.s_teacher_id = teacher_id
    db.session.add(student)
    db.session.commit()


# 教练选择车辆
def teacher_select_car(car_id, teacher_id):
    car = Car.query.get(car_id)
    car.car_teacher_id = teacher_id
    db.session.add(car)
    db.session.commit()
