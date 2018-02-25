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
from .make_data import data_choose_teacher_info, make_week_list, time_convert_timestamp
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
        return render_template('index.html', Student=False, Admin=True, Teacher=False)
    elif current_user.is_anonymous:
        return render_template('index.html', Student=True, Admin=False, Teacher=True)


@app.route('/index_v1', methods=['POST', 'GET'])
def index_v1():
    test_all_3 = Test.query.filter(Test.test_subject == '科目三').order_by(db.desc(Test.test_time)).all()
    test_all_3 = test_all_3[:3]

    test_all_2 = Test.query.filter(Test.test_subject == '科目二').order_by(db.desc(Test.test_time)).all()
    test_all_2 = test_all_2[:3]
    return render_template('index_v1.html', test_all_2=test_all_2, test_all_3=test_all_3)


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
            t_user = User.query.filter_by(id=teacher.t_u_id).first()
            return render_template('update_person_data.html', update_person_user=update_person_user,
                                   update_person_student=update_person_student, is_teacher=True, teacher=teacher,
                                   Student=True,
                                   Teacher=False, t_user=t_user)
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
                                if check_subject(subject):
                                    update_person_info(current_user, user, username, gender, real_name, email, phone,
                                                       identity_number)
                                    update_student_info(current_user, student, subject)
                                    flash('个人资料修改成功')
                                    return redirect(url_for('update_person_data'))
                                else:
                                    flash('所在科目未按要求填写')
                                    return render_template('update_person_data1.html', form=form, Student=True,
                                                           Teacher=False)
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
                if test2_car:
                    test2_car = test2_car.car_number
                else:
                    test2_car = '该教练还未选择车辆'

                test3_car = Car.query.filter(Car.car_teacher_id == teacher.id, Car.car_subject == '科目三').first()
                if test3_car:
                    test3_car = test3_car.car_number
                else:
                    test3_car = '该教练还未选择车辆'
                return render_template('cat_teacher_info.html', real_name=user.real_name, phone=user.phone,
                                       email=user.email, test2_car=test2_car, test3_car=test3_car,
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
            Week_list = []
            make_week_list(Week_list)
            return render_template('release_class_info.html', Week_list=Week_list)
    if request.method == 'POST':
        data = request.get_json()
        if data['am_1'] and data['am_2'] and data['am_3'] and data['am_4'] and data['am_5'] and data['am_6'] and data[
            'am_7'] and data['pm_1'] and data['pm_2'] and data['pm_3'] and data['pm_4'] and data['pm_5'] and data[
            'pm_6'] and data['pm_7']:
            Week_list = []
            make_week_list(Week_list)
            teacher = Teacher.query.filter_by(t_u_id=current_user.id).first()
            teacher_arrange_classes(data, Week_list, teacher.id)
            return jsonify({'ok': 'yes'})
        else:
            return jsonify({'ok': 'no'})


@app.route('/teacher/cat_class_info', methods=['GET'])
def teacher_cat_class_info():
    if request.method == 'GET':
        Week_list = []
        make_week_list(Week_list)

        if current_user.is_anonymous:
            return redirect(url_for('handle_unlogin_request'))
        else:
            teacher = Teacher.query.filter_by(t_u_id=current_user.id).first()
            class_am_1 = Class.query.filter(Class.class_time == Week_list[0], Class.class_pm == None,
                                            Class.class_teacher_id == teacher.id).first()
            class_pm_1 = Class.query.filter(Class.class_time == Week_list[0], Class.class_am == None,
                                            Class.class_teacher_id == teacher.id).first()

            class_am_2 = Class.query.filter(Class.class_time == Week_list[1], Class.class_pm == None,
                                            Class.class_teacher_id == teacher.id).first()
            class_pm_2 = Class.query.filter(Class.class_time == Week_list[1], Class.class_am == None,
                                            Class.class_teacher_id == teacher.id).first()

            class_am_3 = Class.query.filter(Class.class_time == Week_list[2], Class.class_pm == None,
                                            Class.class_teacher_id == teacher.id).first()
            class_pm_3 = Class.query.filter(Class.class_time == Week_list[2], Class.class_am == None,
                                            Class.class_teacher_id == teacher.id).first()

            class_am_4 = Class.query.filter(Class.class_time == Week_list[3], Class.class_pm == None,
                                            Class.class_teacher_id == teacher.id).first()
            class_pm_4 = Class.query.filter(Class.class_time == Week_list[3], Class.class_am == None,
                                            Class.class_teacher_id == teacher.id).first()

            class_am_5 = Class.query.filter(Class.class_time == Week_list[4], Class.class_pm == None,
                                            Class.class_teacher_id == teacher.id).first()
            class_pm_5 = Class.query.filter(Class.class_time == Week_list[4], Class.class_am == None,
                                            Class.class_teacher_id == teacher.id).first()

            class_am_6 = Class.query.filter(Class.class_time == Week_list[5], Class.class_pm == None,
                                            Class.class_teacher_id == teacher.id).first()
            class_pm_6 = Class.query.filter(Class.class_time == Week_list[5], Class.class_am == None,
                                            Class.class_teacher_id == teacher.id).first()

            class_am_7 = Class.query.filter(Class.class_time == Week_list[6], Class.class_pm == None,
                                            Class.class_teacher_id == teacher.id).first()
            class_pm_7 = Class.query.filter(Class.class_time == Week_list[6], Class.class_am == None,
                                            Class.class_teacher_id == teacher.id).first()

            return render_template('teacher_cat_class_info.html', class_am_1=class_am_1, class_pm_1=class_pm_1,
                                   class_am_2=class_am_2, class_pm_2=class_pm_2, class_am_3=class_am_3,
                                   class_pm_3=class_pm_3,
                                   class_am_4=class_am_4, class_pm_4=class_pm_4, class_am_5=class_am_5,
                                   class_pm_5=class_pm_5,
                                   class_am_6=class_am_6, class_pm_6=class_pm_6, class_am_7=class_am_7,
                                   class_pm_7=class_pm_7,
                                   Week_list=Week_list, teacher=teacher)


@app.route('/teacher/cat_car_info', methods=['GET'])
def teacher_cat_car_info():
    if request.method == 'GET':
        if current_user.is_anonymous:
            return redirect(url_for('handle_unlogin_request'))
        else:
            teacher = Teacher.query.filter_by(t_u_id=current_user.id).first()
            car_two = Car.query.filter(Car.car_teacher_id == teacher.id, Car.car_subject == '科目二').first()
            car_three = Car.query.filter(Car.car_teacher_id == teacher.id, Car.car_subject == '科目三').first()
            return render_template('cat_car_info.html', car_two=car_two, car_three=car_three)


@app.route('/teacher/cancel_car', methods=['POST'])
def teacher_cancel_car():
    if request.method == 'POST':
        data = request.get_json()
        car = Car.query.filter_by(id=data['car_id']).first()
        car.car_teacher_id = None
        db.session.add(car)
        db.session.commit()
        return jsonify({'ok': 'yes'})


@app.route('/student/choose_class', methods=['GET'])
def student_choose_class():
    Week_list = []
    make_week_list(Week_list)
    if request.method == 'GET':
        if current_user.is_anonymous:
            return redirect(url_for('handle_unlogin_request'))
        else:
            student = Student.query.filter_by(s_u_id=current_user.id).first()
            teacher = Teacher.query.filter_by(id=student.s_teacher_id).first()
            if teacher:
                class_am_1 = Class.query.filter(Class.class_time == Week_list[0], Class.class_pm == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_am_1:
                    s_am_1 = Student.query.filter(Student.s_am_1_id == class_am_1.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_am_1 = False
                class_pm_1 = Class.query.filter(Class.class_time == Week_list[0], Class.class_am == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_pm_1:
                    s_pm_1 = Student.query.filter(Student.s_pm_1_id == class_pm_1.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_pm_1 = False

                class_am_2 = Class.query.filter(Class.class_time == Week_list[1], Class.class_pm == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_am_2:
                    s_am_2 = Student.query.filter(Student.s_am_2_id == class_am_2.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_am_2 = False
                class_pm_2 = Class.query.filter(Class.class_time == Week_list[1], Class.class_am == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_pm_2:
                    s_pm_2 = Student.query.filter(Student.s_pm_2_id == class_pm_2.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_pm_2 = False

                class_am_3 = Class.query.filter(Class.class_time == Week_list[2], Class.class_pm == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_am_3:
                    s_am_3 = Student.query.filter(Student.s_am_3_id == class_am_3.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_am_3 = False
                class_pm_3 = Class.query.filter(Class.class_time == Week_list[2], Class.class_am == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_pm_3:
                    s_pm_3 = Student.query.filter(Student.s_pm_3_id == class_pm_3.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_pm_3 = False

                class_am_4 = Class.query.filter(Class.class_time == Week_list[3], Class.class_pm == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_am_4:
                    s_am_4 = Student.query.filter(Student.s_am_4_id == class_am_4.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_am_4 = False
                class_pm_4 = Class.query.filter(Class.class_time == Week_list[3], Class.class_am == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_pm_4:
                    s_pm_4 = Student.query.filter(Student.s_pm_4_id == class_pm_4.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_pm_4 = False

                class_am_5 = Class.query.filter(Class.class_time == Week_list[4], Class.class_pm == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_am_5:
                    s_am_5 = Student.query.filter(Student.s_am_5_id == class_am_5.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_am_5 = False
                class_pm_5 = Class.query.filter(Class.class_time == Week_list[4], Class.class_am == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_pm_5:
                    s_pm_5 = Student.query.filter(Student.s_pm_5_id == class_pm_5.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_pm_5 = False

                class_am_6 = Class.query.filter(Class.class_time == Week_list[5], Class.class_pm == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_am_6:
                    s_am_6 = Student.query.filter(Student.s_am_6_id == class_am_6.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_am_6 = False
                class_pm_6 = Class.query.filter(Class.class_time == Week_list[5], Class.class_am == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_pm_6:
                    s_pm_6 = Student.query.filter(Student.s_pm_6_id == class_pm_6.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_pm_6 = False

                class_am_7 = Class.query.filter(Class.class_time == Week_list[6], Class.class_pm == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_am_7:
                    s_am_7 = Student.query.filter(Student.s_am_7_id == class_am_7.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_am_7 = False
                class_pm_7 = Class.query.filter(Class.class_time == Week_list[6], Class.class_am == None,
                                                Class.class_teacher_id == teacher.id).first()
                if class_pm_7:
                    s_pm_7 = Student.query.filter(Student.s_pm_7_id == class_pm_7.id,
                                                  Student.s_u_id == current_user.id).first()
                else:
                    s_pm_7 = False

                t_user = User.query.filter_by(id=teacher.t_u_id).first()

                return render_template('student_choose_class.html', class_am_1=class_am_1, class_pm_1=class_pm_1,
                                       class_am_2=class_am_2, class_pm_2=class_pm_2, class_am_3=class_am_3,
                                       class_pm_3=class_pm_3,
                                       class_am_4=class_am_4, class_pm_4=class_pm_4, class_am_5=class_am_5,
                                       class_pm_5=class_pm_5,
                                       class_am_6=class_am_6, class_pm_6=class_pm_6, class_am_7=class_am_7,
                                       class_pm_7=class_pm_7,
                                       teacher_name=t_user.real_name, Week_list=Week_list, Teacher=True,
                                       s_am_1=s_am_1, s_pm_1=s_pm_1, s_am_2=s_am_2,
                                       s_pm_2=s_pm_2, s_am_3=s_am_3, s_pm_3=s_pm_3, s_am_4=s_am_4, s_pm_4=s_pm_4,
                                       s_am_5=s_am_5, s_pm_5=s_pm_5, s_am_6=s_am_6, s_pm_6=s_pm_6, s_am_7=s_am_7,
                                       s_pm_7=s_pm_7)
            else:
                flash('您还未选择教练')
                return render_template('student_choose_class.html', Teacher=False, Week_list=Week_list)


@app.route('/student/choose_class/confirm', methods=['POST'])
def student_choose_class_confirm():
    if request.method == 'POST':
        data = request.get_json()
        class_id = data['class_id']
        choose_class = Class.query.filter_by(id=class_id).first()
        subject_1 = choose_class.class_am
        subject_2 = choose_class.class_pm
        student = Student.query.filter_by(s_u_id=current_user.id).first()
        if choose_class.class_limit_people <= 0:
            return jsonify({'ok': 'less'})
        else:
            if student.s_subject == subject_1 or student.s_subject == subject_2:
                student_select_class(student, choose_class)
                return jsonify({'ok': 'yes'})
            else:
                return jsonify({'ok': 'no'})


@app.route('/student/cat_class_list', methods=['GET'])
def student_cat_class_list():
    if request.method == 'GET':
        if current_user.is_anonymous:
            return redirect(url_for('handle_unlogin_request'))
        else:
            Week_list = []
            make_week_list(Week_list)
            student = Student.query.filter_by(s_u_id=current_user.id).first()
            class_am_1 = Class.query.filter(Class.id == student.s_am_1_id, Class.class_time == Week_list[0]).first()
            class_am_2 = Class.query.filter(Class.id == student.s_am_2_id, Class.class_time == Week_list[1]).first()
            class_am_3 = Class.query.filter(Class.id == student.s_am_3_id, Class.class_time == Week_list[2]).first()
            class_am_4 = Class.query.filter(Class.id == student.s_am_4_id, Class.class_time == Week_list[3]).first()
            class_am_5 = Class.query.filter(Class.id == student.s_am_5_id, Class.class_time == Week_list[4]).first()
            class_am_6 = Class.query.filter(Class.id == student.s_am_6_id, Class.class_time == Week_list[5]).first()
            class_am_7 = Class.query.filter(Class.id == student.s_am_7_id, Class.class_time == Week_list[6]).first()
            class_pm_1 = Class.query.filter(Class.id == student.s_pm_1_id, Class.class_time == Week_list[0]).first()
            class_pm_2 = Class.query.filter(Class.id == student.s_pm_2_id, Class.class_time == Week_list[1]).first()
            class_pm_3 = Class.query.filter(Class.id == student.s_pm_3_id, Class.class_time == Week_list[2]).first()
            class_pm_4 = Class.query.filter(Class.id == student.s_pm_4_id, Class.class_time == Week_list[3]).first()
            class_pm_5 = Class.query.filter(Class.id == student.s_pm_5_id, Class.class_time == Week_list[4]).first()
            class_pm_6 = Class.query.filter(Class.id == student.s_pm_6_id, Class.class_time == Week_list[5]).first()
            class_pm_7 = Class.query.filter(Class.id == student.s_pm_7_id, Class.class_time == Week_list[6]).first()


            return render_template('student_cat_class_list.html', Week_list=Week_list, class_am_1=class_am_1,
                                   class_am_2=class_am_2, class_am_3=class_am_3, class_am_4=class_am_4,
                                   class_am_5=class_am_5, class_am_6=class_am_6, class_am_7=class_am_7,
                                   class_pm_1=class_pm_1, class_pm_2=class_pm_2, class_pm_3=class_pm_3,
                                   class_pm_4=class_pm_4, class_pm_5=class_pm_5, class_pm_6=class_pm_6,
                                   class_pm_7=class_pm_7)


@app.route('/student/cancel_class', methods=['POST'])
def student_cancel_class():
    if request.method == 'POST':
        data = request.get_json()
        class_id = data['class_id']
        choose_class = Class.query.filter_by(id=class_id).first()
        student = Student.query.filter_by(s_u_id=current_user.id).first()
        student_cancel_selected_class(student, choose_class)
        return jsonify({'ok': 'yes'})


@app.route('/admin/public/test', methods=['POST', 'GET'])
def admin_public_test():
    if request.method == 'GET':
        return render_template('admin_pub_test.html')
    if request.method == 'POST':
        data = request.get_json()
        subject = data['subject']
        test_time = data['test_time']
        sign_end_time = data['sign_end_time']
        sign_start_time = data['sign_start_time']

        if subject == '科目二' or subject == '科目三':
            if test_time != '' and sign_end_time != '' and sign_start_time != '':
                convert_test_time = time_convert_timestamp(test_time)
                convert_sign_start_time = time_convert_timestamp(sign_start_time)
                convert_sign_end_time = time_convert_timestamp(sign_end_time)
                if convert_sign_start_time < convert_sign_end_time and convert_test_time > convert_sign_end_time:
                    test = Test.query.filter(Test.test_subject == subject, Test.test_time == test_time).first()
                    today = str(date.today())

                    today = time_convert_timestamp(today)
                    if today < convert_test_time:
                        if not test:
                            admin_pub_test_time(subject, test_time, sign_start_time, sign_end_time)
                            return jsonify({'ok': 'yes'})

                        else:
                            return jsonify({'ok': 'exist'})
                    else:
                        return jsonify({'ok': 'time_pass'})
                else:
                    return jsonify({'ok': 'date_error'})

            else:
                return jsonify({'ok': 'data_no'})

        else:
            return jsonify({'ok': 'error_subject'})


@app.route('/admin/cat/test2', methods=['GET'])
def admin_cat_test2():
    if request.method == 'GET':
        today = str(date.today())
        today = time_convert_timestamp(today)
        test_all = Test.query.filter(Test.test_subject == '科目二').order_by(db.desc(Test.test_time)).all()
        test_all = test_all[:8]
        test = []
        for each in test_all:
            if time_convert_timestamp(str(each.test_time)) > today:
                test.append(each)

        return render_template('admin_cat_test2.html', test=test)


@app.route('/admin/cat/test3', methods=['GET'])
def admin_cat_test3():
    if request.method == 'GET':
        today = str(date.today())
        today = time_convert_timestamp(today)
        test_all = Test.query.filter(Test.test_subject == '科目三').order_by(db.desc(Test.test_time)).all()
        test_all = test_all[:8]
        test = []
        for each in test_all:
            if time_convert_timestamp(str(each.test_time)) > today:
                test.append(each)
                print(each.sign_number)

        return render_template('admin_cat_test3.html', test=test)


@app.route('/student/choose_test2', methods=['GET', 'POST'])
def student_choose_test2():
    if request.method == 'GET':
        if current_user.is_anonymous:
            return redirect(url_for('unlogin'))
        else:
            student = Student.query.filter_by(s_u_id=current_user.id).first()
            if student.s_subject != '科目二':
                return redirect(url_for('student_error_test'))
            elif student.s_subject == '科目二':
                today = str(date.today())
                today = time_convert_timestamp(today)
                test_all = Test.query.filter(Test.test_subject == '科目二').all()
                test = []
                for each in test_all:
                    if time_convert_timestamp(str(each.test_time)) > today:
                        test.append(each)
                return render_template('student_choose_test2.html', test=test)
    if request.method == 'POST':
        data = request.get_json()
        test_id = data['test_id']
        student = Student.query.filter_by(s_u_id=current_user.id).first()
        test = Test.query.filter_by(id=test_id).first()
        today = str(date.today())
        today = time_convert_timestamp(today)
        if student.s_test_2_id:

            last_test = Test.query.filter_by(id=student.s_test_2_id).first()
            if today > time_convert_timestamp(str(test.sign_start_time)) and time_convert_timestamp(
                    str(test.sign_end_time)):
                if today > time_convert_timestamp(str(last_test.test_time)):
                    student.s_test_2_id = test_id
                    db.session.add(student)
                    db.session.commit()
                    test.sign_number += 1
                    db.session.add(test)
                    db.session.commit()

                    return jsonify({'ok': 'yes'})
                else:
                    return jsonify({'ok': 'last'})
            else:
                return jsonify({'ok': 'error_sign_time'})
        else:
            if today > time_convert_timestamp(str(test.sign_start_time)) and time_convert_timestamp(
                    str(test.sign_end_time)):
                student.s_test_2_id = test_id
                db.session.add(student)
                db.session.commit()
                test.sign_number += 1
                db.session.add(test)
                db.session.commit()
                return jsonify({'ok': 'yes'})
            else:
                return jsonify({'ok': 'error_sign_time'})



@app.route('/student/choose_test3', methods=['GET', 'POST'])
def student_choose_test3():
    if request.method == 'GET':
        if current_user.is_anonymous:
            return redirect(url_for('unlogin'))
        else:
            student = Student.query.filter_by(s_u_id=current_user.id).first()
            if student.s_subject != '科目三':
                return redirect(url_for('student_error_test'))
            elif student.s_subject == '科目三':
                today = str(date.today())
                today = time_convert_timestamp(today)
                test_all = Test.query.filter(Test.test_subject == '科目三').all()
                test = []
                for each in test_all:
                    if time_convert_timestamp(str(each.test_time)) > today:
                        test.append(each)
                return render_template('student_choose_test3.html', test=test)
    if request.method == 'POST':
        data = request.get_json()
        test_id = data['test_id']
        student = Student.query.filter_by(s_u_id=current_user.id).first()
        test = Test.query.filter_by(id=test_id).first()
        today = str(date.today())
        today = time_convert_timestamp(today)
        if student.s_test_3_id:
            last_test = Test.query.filter_by(id=student.s_test_3_id).first()
            if today > time_convert_timestamp(str(test.sign_start_time)) and time_convert_timestamp(str(test.sign_end_time)):
                if today > time_convert_timestamp(str(last_test.test_time)):
                    student.s_test_3_id = test_id
                    db.session.add(student)
                    db.session.commit()
                    test.sign_number += 1
                    db.session.add(test)
                    db.session.commit()

                    return jsonify({'ok': 'yes'})
                else:
                    return jsonify({'ok': 'last'})
            else:
                return jsonify({'ok': 'error_sign_time'})
        else:
            if today > time_convert_timestamp(str(test.sign_start_time)) and time_convert_timestamp(
                    str(test.sign_end_time)):
                student.s_test_3_id = test_id
                db.session.add(student)
                db.session.commit()
                test.sign_number += 1
                db.session.add(test)
                db.session.commit()
                return jsonify({'ok': 'yes'})
            else:
                return jsonify({'ok': 'error_sign_time'})


@app.route('/student/error_test', methods=['GET'])
def student_error_test():
    if request.method == 'GET':
        return render_template('student_error_test.html')


@app.route('/student/cat/test_info', methods=['GET'])
def student_cat_test_info():
    if request.method == 'GET':
        if request.method == 'GET':
            if current_user.is_anonymous:
                return redirect(url_for('unlogin'))
            else:
                student = Student.query.filter_by(s_u_id=current_user.id).first()
                if student.s_subject == '科目二':
                    test = Test.query.filter_by(id=student.s_test_2_id).first()
                    return render_template('student_cat_test_info.html', test=test)
                elif student.s_subject == '科目三':
                    test = Test.query.filter_by(id=student.s_test_3_id).first()
                    return render_template('student_cat_test_info.html', test=test)


@app.route('/teacher/cat/student_process', methods=['GET'])
def teacher_cat_student_process():
    if request.method == 'GET':
        if request.method == 'GET':
            if current_user.is_anonymous:
                return redirect(url_for('unlogin'))
            else:
                teacher = Teacher.query.filter_by(t_u_id=current_user.id).first()
                student = Student.query.filter_by(s_teacher_id=teacher.id).all()
                process = {}
                n = 0

                for each in student:
                    new_user = User.query.filter_by(id=each.s_u_id).first()
                    if each.s_subject == '科目二':
                        new_test = Test.query.filter_by(id=each.s_test_2_id).first()
                    if each.s_subject == '科目三':
                        new_test = Test.query.filter_by(id=each.s_test_3_id).first()
                    process.setdefault(n, [])
                    process[n].append(new_user)
                    process[n].append(each)
                    process[n].append(new_test)
                    n += 1

                return render_template('teacher_cat_student_process.html', process=process)
