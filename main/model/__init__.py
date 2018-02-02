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
from datetime import datetime

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


# 学员所在科目填写检查
def check_subject(student_subject):
    if student_subject == '科目二' or student_subject == '科目三':
        return student_subject
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


# 教练排课
def teacher_arrange_classes(data, week_list, teacher_id):
    # 周一课程
    class_1 = Class.query.filter(Class.class_time == week_list[0], Class.class_teacher_id == teacher_id).all()
    if class_1:
        class_am_11 = Class.query.filter(Class.class_time == week_list[0], Class.class_pm == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_am_11.class_am = data['am_1']
        db.session.add(class_am_11)
        db.session.commit()
        class_pm_11 = Class.query.filter(Class.class_time == week_list[0], Class.class_am == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_pm_11.class_pm = data['pm_1']
        db.session.add(class_pm_11)
        db.session.commit()
    else:
        class_am_1 = Class(
            class_time=week_list[0],
            class_am=data['am_1'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_am_1)
        db.session.commit()

        class_pm_1 = Class(
            class_time=week_list[0],
            class_pm=data['pm_1'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_pm_1)
        db.session.commit()

    # 周二课程
    class_2 = Class.query.filter(Class.class_time == week_list[1], Class.class_teacher_id == teacher_id).all()
    if class_2:
        class_am_22 = Class.query.filter(Class.class_time == week_list[1], Class.class_pm == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_am_22.class_am = data['am_2']
        db.session.add(class_am_22)
        db.session.commit()
        class_pm_22 = Class.query.filter(Class.class_time == week_list[1], Class.class_am == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_pm_22.class_pm = data['pm_2']
        db.session.add(class_pm_22)
        db.session.commit()
    else:
        class_am_2 = Class(
            class_time=week_list[1],
            class_am=data['am_2'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_am_2)
        db.session.commit()

        class_pm_2 = Class(
            class_time=week_list[1],
            class_pm=data['pm_2'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_pm_2)
        db.session.commit()
    # 周三课程
    class_3 = Class.query.filter(Class.class_time == week_list[2], Class.class_teacher_id == teacher_id).all()
    if class_3:
        class_am_33 = Class.query.filter(Class.class_time == week_list[2], Class.class_pm == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_am_33.class_am = data['am_3']
        db.session.add(class_am_33)
        db.session.commit()
        class_pm_33 = Class.query.filter(Class.class_time == week_list[2], Class.class_am == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_pm_33.class_pm = data['pm_3']
        db.session.add(class_pm_33)
        db.session.commit()
    else:
        class_am_3 = Class(
            class_time=week_list[2],
            class_am=data['am_3'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_am_3)
        db.session.commit()

        class_pm_3 = Class(
            class_time=week_list[2],
            class_pm=data['pm_3'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_pm_3)
        db.session.commit()
    # 周四课程
    class_4 = Class.query.filter(Class.class_time == week_list[3], Class.class_teacher_id == teacher_id).all()
    if class_4:
        class_am_44 = Class.query.filter(Class.class_time == week_list[3], Class.class_pm == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_am_44.class_am = data['am_4']
        db.session.add(class_am_44)
        db.session.commit()
        class_pm_44 = Class.query.filter(Class.class_time == week_list[3], Class.class_am == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_pm_44.class_pm = data['pm_4']
        db.session.add(class_pm_44)
        db.session.commit()
    else:
        class_am_4 = Class(
            class_time=week_list[3],
            class_am=data['am_4'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_am_4)
        db.session.commit()

        class_pm_4 = Class(
            class_time=week_list[3],
            class_pm=data['pm_4'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_pm_4)
        db.session.commit()

    # 周五课程
    class_5 = Class.query.filter(Class.class_time == week_list[4], Class.class_teacher_id == teacher_id).all()
    if class_5:
        class_am_55 = Class.query.filter(Class.class_time == week_list[4], Class.class_pm == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_am_55.class_am = data['am_5']
        db.session.add(class_am_55)
        db.session.commit()
        class_pm_55 = Class.query.filter(Class.class_time == week_list[4], Class.class_am == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_pm_55.class_pm = data['pm_5']
        db.session.add(class_pm_55)
        db.session.commit()
    else:
        class_am_5 = Class(
            class_time=week_list[4],
            class_am=data['am_5'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_am_5)
        db.session.commit()

        class_pm_5 = Class(
            class_time=week_list[4],
            class_pm=data['pm_5'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_pm_5)
        db.session.commit()
    # 周六课程
    class_6 = Class.query.filter(Class.class_time == week_list[5], Class.class_teacher_id == teacher_id).all()
    if class_6:
        class_am_66 = Class.query.filter(Class.class_time == week_list[5], Class.class_pm == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_am_66.class_am = data['am_6']
        db.session.add(class_am_66)
        db.session.commit()
        class_pm_66 = Class.query.filter(Class.class_time == week_list[5], Class.class_am == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_pm_66.class_pm = data['pm_6']
        db.session.add(class_pm_66)
        db.session.commit()
    else:
        class_am_6 = Class(
            class_time=week_list[5],
            class_am=data['am_6'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_am_6)
        db.session.commit()

        class_pm_6 = Class(
            class_time=week_list[5],
            class_pm=data['pm_6'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_pm_6)
        db.session.commit()

    # 周日课程
    class_7 = Class.query.filter(Class.class_time == week_list[6], Class.class_teacher_id == teacher_id).all()
    if class_7:
        class_am_77 = Class.query.filter(Class.class_time == week_list[6], Class.class_pm == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_am_77.class_am = data['am_7']
        db.session.add(class_am_77)
        db.session.commit()
        class_pm_77 = Class.query.filter(Class.class_time == week_list[6], Class.class_am == None,
                                         Class.class_teacher_id == teacher_id).first()
        class_pm_77.class_pm = data['pm_7']
        db.session.add(class_pm_77)
        db.session.commit()
    else:
        class_am_7 = Class(
            class_time=week_list[6],
            class_am=data['am_7'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_am_7)
        db.session.commit()

        class_pm_7 = Class(
            class_time=week_list[6],
            class_pm=data['pm_7'],
            class_teacher_id=teacher_id,
            class_limit_people=8
        )
        db.session.add(class_pm_7)
        db.session.commit()


# 学生选课
def student_select_class(student, choose_class):
    number = choose_class.class_time.weekday() + 1
    if choose_class.class_am:
        if number == 1:
            student.s_am_1_id = choose_class.id
        elif number == 2:
            student.s_am_2_id = choose_class.id
        elif number == 3:
            student.s_am_3_id = choose_class.id
        elif number == 4:
            student.s_am_4_id = choose_class.id
        elif number == 5:
            student.s_am_5_id = choose_class.id
        elif number == 6:
            student.s_am_6_id = choose_class.id
        elif number == 7:
            student.s_am_7_id = choose_class.id
    else:
        if number == 1:
            student.s_pm_1_id = choose_class.id
        elif number == 2:
            student.s_pm_2_id = choose_class.id
        elif number == 3:
            student.s_pm_3_id = choose_class.id
        elif number == 4:
            student.s_pm_4_id = choose_class.id
        elif number == 5:
            student.s_pm_5_id = choose_class.id
        elif number == 6:
            student.s_pm_6_id = choose_class.id
        elif number == 7:
            student.s_pm_7_id = choose_class.id
    db.session.add(student)
    db.session.commit()
    choose_class.class_limit_people -= 1
    db.session.add(choose_class)
    db.session.commit()


# 学生取消选课
def student_cancel_selected_class(student, choose_class):
    number = choose_class.class_time.weekday() + 1
    if choose_class.class_am:
        if number == 1:
            student.s_am_1_id = None
        elif number == 2:
            student.s_am_2_id = None
        elif number == 3:
            student.s_am_3_id = None
        elif number == 4:
            student.s_am_4_id = None
        elif number == 5:
            student.s_am_5_id = None
        elif number == 6:
            student.s_am_6_id = None
        elif number == 7:
            student.s_am_7_id = None
    else:
        if number == 1:
            student.s_pm_1_id = None
        elif number == 2:
            student.s_pm_2_id = None
        elif number == 3:
            student.s_pm_3_id = None
        elif number == 4:
            student.s_pm_4_id = None
        elif number == 5:
            student.s_pm_5_id = None
        elif number == 6:
            student.s_pm_6_id = None
        elif number == 7:
            student.s_pm_7_id = None
    db.session.add(student)
    db.session.commit()
    choose_class.class_limit_people += 1
    db.session.add(choose_class)
    db.session.commit()
