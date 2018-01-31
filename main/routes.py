from flask import Flask, jsonify, render_template, redirect, url_for, request, send_file, flash, Response
from flask import session
from . import app
from . import *
from .form import RegistForm, LoginForm, UpdateForm
from .model import *
from .model.user import User
from hashlib import md5
from flask_security.utils import login_user, logout_user
from flask_login import login_required
from flask_security import current_user
from .make_data import data_choose_teacher_info
from datetime import datetime, date, timedelta


@app.route("/login", methods=['GET', 'POST'])
@app.route("/", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    user1 = User.query.filter_by(username=form.username.data).first()

    if form.validate_on_submit():
        if user1 is None:
            flash('该用户不存在')
            return render_template('login.html', user1=user1, form=form)
        else:
            l_password = md5((form.password.data + user1.salt).encode('utf-8')).hexdigest()
            if user1.password == l_password:
                login_user(user1, remember=True)
                return redirect(url_for('index'))

            else:
                flash('密码错误')
                return render_template('login.html', user1=user1, form=form)

    return render_template('login.html', user1=user1, form=form)


@app.route('/index', methods=['POST', 'GET'])
def index():
    if current_user.has_role('Student'):
        return render_template('index.html', Student=True, Admin=False, Teacher=False)

    elif current_user.has_role('Teacher'):
        return render_template('index.html', Student=False, Admin=False, Teacher=True)
    elif current_user.has_role('Admin'):
        return render_template('index.html', Student=True, Admin=True, Teacher=True)
    elif current_user.is_anonymous:
        return render_template('index.html', Student=True, Admin=False, Teacher=True)


@app.route('/index_v1', methods=['POST', 'GET'])
def index_v1():
    return render_template('index_v1.html')


@app.route('/regist', methods=['POST', 'GET'])
def regist():
    form = RegistForm()
    username = form.r_username.data
    password = form.r_password.data
    phone = form.phone.data
    email = form.email.data
    role_name = form.role.data
    user = User.query.filter_by(username=username).first()

    if form.validate_on_submit():
        if not user:
            if password == form.rr_password.data:
                if check_phone(phone) is not None and check_email(email) is not None:
                    confirm_regist(username, password, phone, email, role_name)
                    regist_user = User.query.filter_by(username=username).first()
                    login_user(regist_user)
                    flash('新增成功')
                    return render_template('regist.html', form=form)

                else:
                    flash('电话或者邮箱格式错误')
                    return render_template('regist.html', form=form)
            else:
                flash('两次密码不一致')
                return render_template('regist.html', form=form)
        else:
            flash('用户名已存在')
            return render_template('regist.html', form=form)
    return render_template('regist.html', form=form)


@app.route('/update_person_data', methods=['GET'])
def update_person_data():
    if current_user.is_anonymous:
        return redirect(url_for('unlogin'))
    elif current_user.has_role('Student'):
        update_person_user = User.query.get(current_user.id)
        update_person_student = Student.query.filter_by(s_u_id=update_person_user.id).first()
        teacher = Teacher.query.filter_by(id=update_person_student.s_teacher_id).first()
        if teacher:
            return render_template('update_person_data.html', update_person_user=update_person_user,
                                   update_person_student=update_person_student, is_teacher=True, teacher=teacher,
                                   Student=True,
                                   Teacher=False)
        else:
            return render_template('update_person_data.html', update_person_user=update_person_user,
                                   update_person_student=update_person_student, Student=True,
                                   Teacher=False, is_teacher=False)
    elif current_user.has_role('Teacher'):
        update_person_user = User.query.get(current_user.id)
        update_person_teacher = Teacher.query.filter_by(t_u_id=update_person_user.id).first()
        return render_template('update_person_data.html', update_person_user=update_person_user,
                               update_person_teacher=update_person_teacher, Student=False,
                               Teacher=True, is_teacher=False)
    else:
        update_person_user = User.query.get(current_user.id)
        return render_template('update_person_data.html', update_person_user=update_person_user, Student=False,
                               Teacher=False, is_teacher=False)


@app.route('/no_permission', methods=['GET', 'POST'])
def no_permission():
    return render_template('no_permission.html')


@app.route('/update_person_data1', methods=['POST', 'GET'])
def update_person_data1():
    form = RegistForm()
    if request.method == 'GET':
        if current_user.is_anonymous:
            return redirect(url_for('unlogin'))
        elif current_user.has_role('Student'):
            return render_template('update_person_data1.html', Student=True, Teacher=False, form=form)
        elif current_user.has_role('Teacher'):
            return render_template('update_person_data1.html', Student=False, Teacher=True, form=form)
        else:
            return render_template('update_person_data1.html', Student=False, Teacher=False, form=form)

    elif request.method == 'POST':
        username = form.update_username.data
        gender = form.gender.data
        real_name = form.real_name.data
        email = form.update_email.data
        phone = form.update_phone.data
        identity_number = form.identity_number.data
        if current_user.has_role('Student'):
            user = User.query.get(current_user.id)
            student = Student.query.filter_by(s_u_id=current_user.id).first()
            subject = form.subject.data
            if check_gender(gender):
                if check_real_name(real_name):
                    if check_email(email):
                        if check_phone(phone):
                            if check_identity_number(identity_number):
                                update_person_info(current_user, user, username, gender, real_name, email, phone,
                                                   identity_number)
                                update_student_info(current_user, student, subject)
                                flash('个人资料修改成功')
                                return redirect(url_for('update_person_data'))
                            else:
                                flash('身份证格式或长度错误')
                                return render_template('update_person_data1.html', form=form, Student=True,
                                                       Teacher=False)

                        else:
                            flash('电话号码格式错误')
                            return render_template('update_person_data1.html', form=form, Student=True, Teacher=False)
                    else:
                        flash('邮箱格式错误')
                        return render_template('update_person_data1.html', form=form, Student=True, Teacher=False)
                else:
                    flash('姓名格式或长度不正确')
                    return render_template('update_person_data1.html', form=form, Student=True, Teacher=False)
            else:
                flash('性别格式错误')
            return render_template('update_person_data1.html', form=form, Student=True, Teacher=False)

        if current_user.has_role('Teacher'):
            user = User.query.get(current_user.id)
            teacher = Teacher.query.filter_by(t_u_id=current_user.id).first()
            work_time = form.work_time.data
            if check_gender(gender):
                if check_real_name(real_name):
                    if check_email(email):
                        if check_phone(phone):
                            if check_identity_number(identity_number):
                                update_person_info(current_user, user, username, gender, real_name, email, phone,
                                                   identity_number)
                                update_teacher_info(current_user, teacher, work_time)
                                flash('个人资料修改成功')
                                return redirect(url_for('update_person_data'))
                            else:
                                flash('身份证格式或长度错误')
                                return render_template('update_person_data1.html', Student=False, Teacher=True,
                                                       form=form)

                        else:
                            flash('电话号码格式错误')
                            return render_template('update_person_data1.html', Student=False, Teacher=True, form=form)
                    else:
                        flash('邮箱格式错误')
                        return render_template('update_person_data1.html', Student=False, Teacher=True, form=form)
                else:
                    flash('姓名格式或长度不正确')
                    return render_template('update_person_data1.html', Student=False, Teacher=True, form=form)
            else:
                flash('性别格式错误')
                return render_template('update_person_data1.html', Student=False, Teacher=True, form=form)

        if current_user.has_role('Admin'):
            user = User.query.get(current_user.id)
            if check_gender(gender):
                if check_real_name(real_name):
                    if check_email(email):
                        if check_phone(phone):
                            if check_identity_number(identity_number):
                                update_person_info(current_user, user, username, gender, real_name, email, phone,
                                                   identity_number)

                                flash('个人资料修改成功')
                                return redirect(url_for('update_person_data'))
                            else:
                                flash('身份证格式或长度错误或者已存在')
                                return render_template('update_person_data1.html', Student=False, Teacher=False,
                                                       form=form)


                        else:
                            flash('电话号码格式错误')
                            return render_template('update_person_data1.html', Student=False, Teacher=False, form=form)

                    else:
                        flash('邮箱格式错误')
                        return render_template('update_person_data1.html', Student=False, Teacher=False, form=form)

                else:
                    flash('姓名格式或长度不正确')
                    return render_template('update_person_data1.html', Student=False, Teacher=False, form=form)

            else:
                flash('性别格式错误')
                return render_template('update_person_data1.html', Student=False, Teacher=False, form=form)


@app.route('/update_person_passwd', methods=['POST', 'GET'])
def update_person_passwd():
    form = UpdateForm()

    if request.method == 'GET':
        if current_user.is_anonymous:
            return redirect(url_for('unlogin'))
        else:
            return render_template('update_person_passwd.html', form=form)
    elif request.method == 'POST':
        user = User.query.filter_by(username=current_user.username).first()
        if form.u_password.data == form.ru_password.data:
            user.password = md5((form.u_password.data + user.salt).encode('utf-8')).hexdigest()
            db.session.add(user)
            db.session.commit()
            flash('修改成功')
            return render_template('update_person_passwd.html', form=form)
        else:
            flash('两次密码不一致')
            return render_template('update_person_passwd.html', form=form)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for('index_v1'))


@app.route('/unlogin', methods=['POST', 'GET'])
def unlogin():
    return render_template('unlogin.html')


@app.route('/confirm_admin', methods=['GET'])
def confirm_admin():
    if request.method == 'GET':
        if current_user.has_role('Admin'):
            return redirect(url_for('admin.index'))
        else:
            return redirect(url_for('no_permission'))


@app.route('/user_validation', methods=['GET', 'POST'])
def user_validation():
    form = RegistForm()
    if request.method == 'POST':
        validation_user = User.query.filter_by(username=form.r_username.data).first()
        if validation_user:
            if form.email.data == validation_user.email:
                session['username'] = request.form['r_username']
                return redirect(url_for('forget_password'))
            else:
                flash('邮箱错误')
                return render_template('validation_email.html', form=form)
        else:
            flash('该用户不存在')
            return render_template('validation_email.html', form=form)
    return render_template('validation_email.html', form=form, username=session.get('username'))


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = RegistForm()
    forget_username = session['username']
    forget_user = User.query.filter_by(username=forget_username).first()
    if request.method == 'POST':

        if form.r_password.data == form.rr_password.data:
            forget_user.password = md5((form.r_password.data + forget_user.salt).encode('utf-8')).hexdigest()
            db.session.add(forget_user)
            db.session.commit()
            flash('重置密码成功')
            return render_template('forget_password.html', form=form)
        else:
            flash('两次密码不一致')
            return render_template('forget_password.html', form=form)

    return render_template('forget_password.html', form=form)


@app.route('/student/choose_teacher', methods=['GET', 'POST'])
def student_choose_teacher():
    teacher = Teacher.query.all()
    new_data = []
    data_choose_teacher_info(new_data, teacher)
    if request.method == 'GET':
        if current_user.has_role('Student'):
            student = Student.query.filter_by(s_u_id=current_user.id).first()
            if student.s_teacher_id:

                return render_template('choose_teacher.html', new_data=new_data, Button=False)
            else:

                return render_template('choose_teacher.html', new_data=new_data, Button=True)

        else:
            return redirect(url_for('no_permission'))
    if request.method == 'POST':
        data = request.get_json()
        teacher_id = data['teacher_id']
        student_select_teacher(teacher_id, current_user.id)
        data = {}
        data['ok'] = 'yes'
        return jsonify(data)


@app.route('/teacher/choose_car/test2', methods=['GET', 'POST'])
def teacher_choose_car_test2():
    if request.method == 'GET':
        if current_user.has_role('Teacher'):
            teacher = Teacher.query.filter_by(t_u_id=current_user.id).first()
            cars = Car.query.filter_by(car_subject='科目二').all()
            teacher_car = Car.query.filter(Car.car_teacher_id == teacher.id, Car.car_subject == '科目二').first()

            for car in cars:
                if car.car_teacher_id:
                    cars.remove(car)
            if teacher_car:
                return render_template('choose_test2_car.html', cars=cars, Button=False)
            else:
                return render_template('choose_test2_car.html', cars=cars, Button=True)

        else:
            return redirect(url_for('no_permission'))
    if request.method == 'POST':
        data = request.get_json()
        car_id = data['car_id']
        teacher = Teacher.query.filter_by(t_u_id=current_user.id).first()
        teacher_select_car(car_id, teacher.id)
        return jsonify({'ok': 'yes'})


@app.route('/teacher/choose_car/test3', methods=['GET', 'POST'])
def teacher_choose_car_test3():
    if request.method == 'GET':
        if current_user.has_role('Teacher'):
            teacher = Teacher.query.filter_by(t_u_id=current_user.id).first()
            cars = Car.query.filter_by(car_subject='科目三').all()
            teacher_car = Car.query.filter(Car.car_teacher_id == teacher.id, Car.car_subject == '科目三').first()

            for car in cars:
                if car.car_teacher_id:
                    cars.remove(car)
            if teacher_car:
                return render_template('choose_test3_car.html', cars=cars, Button=False)
            else:
                return render_template('choose_test3_car.html', cars=cars, Button=True)

        else:
            return redirect(url_for('no_permission'))
    if request.method == 'POST':
        data = request.get_json()
        car_id = data['car_id']
        teacher = Teacher.query.filter_by(t_u_id=current_user.id).first()
        teacher_select_car(car_id, teacher.id)
        return jsonify({'ok': 'yes'})


@app.route('/student/cat/teacher_info', methods=['GET'])
def student_cat_teacher_info():
    if request.method == 'GET':
        if current_user.has_role('Student'):
            student = Student.query.filter_by(s_u_id=current_user.id).first()
            teacher = Teacher.query.filter_by(id=student.s_teacher_id).first()
            if teacher:
                user = User.query.get(teacher.t_u_id)
                test2_car = Car.query.filter(Car.car_teacher_id == teacher.id, Car.car_subject == '科目二').first()
                test3_car = Car.query.filter(Car.car_teacher_id == teacher.id, Car.car_subject == '科目三').first()
                return render_template('cat_teacher_info.html', real_name=user.real_name, phone=user.phone,
                                       email=user.email, test2_car=test2_car.car_number, test3_car=test3_car.car_number,
                                       Teacher_info=True, username=user.username)
            else:
                return render_template('cat_teacher_info.html', Teacher_info=False)
        else:
            return redirect(url_for('no_permission'))


@app.route('/teacher/release_class_info', methods=['POST', 'GET'])
def teacher_release_class_info():
    if request.method == 'GET':
        if current_user.is_anonymous:
            return redirect(url_for('handle_unlogin_request'))
        else:
            today = date.today()
            Sunday = today + timedelta(6 - today.weekday())
            Monday = today - timedelta(today.weekday())
            return render_template('release_class_info.html', monday=Monday, sunday=Sunday)
    if request.method == 'POST':
        data = request.get_json()
        if data['am_1'] and data['am_2'] and data['am_3'] and data['am_4'] and data['am_5'] and data['am_6'] and data['am_7'] and data['pm_1'] and data['pm_2'] and data['pm_3'] and data['pm_4'] and data['pm_5'] and data['pm_6'] and data['pm_7']:
            today = date.today()
            Monday = today - timedelta(today.weekday())
            Week_list = []
            for i in range(7):
                Week_list.append(Monday + timedelta(i))
            teacher = Teacher.query.filter_by(t_u_id=current_user.id).first()
            teacher_arrange_classes(data, Week_list, teacher.id)
            return jsonify({'ok': 'yes'})
        else:
            return jsonify({'ok': 'no'})
