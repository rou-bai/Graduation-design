from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField, IntegerField


class LoginForm(FlaskForm):
    username = StringField(u'用户名',
                           render_kw={'placeholder': '用户名',
                                      'class': 'form-control'})
    password = PasswordField(u'密码',
                             render_kw={'placeholder': '密码',
                                        'class': 'form-control'})
    remember_me = BooleanField('记住账号密码',
                               render_kw={'class': 'i-checks'})
    submit = SubmitField(u'登录',
                         render_kw={'class': 'btn btn-success btn-block'})


class RegistForm(FlaskForm):
    r_username = StringField('用户名',
                             render_kw={'placeholder': '用户名',
                                        'class': 'form-control',
                                        'required': 'required'})
    update_username = StringField('用户名',
                                  render_kw={
                                      'class': 'form-control',
                                      'required': 'required'})
    r_password = PasswordField('密码',
                               render_kw={'placeholder': '密码',
                                          'class': 'form-control',
                                          'required': 'required'
                                          })
    rr_password = PasswordField('请再次输入密码',
                                render_kw={'placeholder': '请重新输入密码',
                                           'class': 'form-control',
                                           'required': 'required'
                                           })
    phone = StringField('电话号码',
                        render_kw={'placeholder': '电话号码',
                                   'class': 'form-control',
                                   'required': 'required'
                                   })
    update_phone = StringField('电话号码',
                               render_kw={
                                   'class': 'form-control',
                                   'required': 'required'
                               })
    email = StringField('邮箱',
                        render_kw={'placeholder': '邮箱',
                                   'class': 'form-control',
                                   'required': 'required'
                                   })
    update_email = StringField('邮箱',
                               render_kw={
                                   'class': 'form-control',
                                   'required': 'required'
                               })
    role = SelectField('用户类型',
                       choices=[('1', '学员'), ('2', '教练')],
                       render_kw={'class': 'print_page form-control m-b'})
    accept_terms = BooleanField('我同意注册协议', default='checked',
                                render_kw={'class': 'i-checks',
                                           'required': 'required'
                                           })

    r_submit = SubmitField('注册',
                           render_kw={'placeholder': '注册',
                                      'class': 'btn btn-primary block full-width m-b'})
    u_submit = SubmitField('修改',
                           render_kw={'placeholder': '修改',
                                      'class': 'btn btn-primary block full-width m-b'})
    p_submit = SubmitField('确认',
                           render_kw={'placeholder': '确认',
                                      'class': 'btn btn-primary block full-width m-b'})
    real_name = StringField('真实姓名',
                            render_kw={'class': 'form-control',
                                       'required': 'required'})
    subject = StringField('学员科目进度',
                          render_kw={'class': 'form-control',
                                     'required': 'required'}
                          )
    gender = StringField('性别',
                         render_kw={'class': 'form-control',
                                    'required': 'required'})
    identity_number = StringField('身份证号码',
                                   render_kw={'class': 'form-control',
                                              'required': 'required'}
                                   )
    work_time = StringField('工龄', render_kw={'class': 'form-control',
                                             'required': 'required'})


class UpdateForm(FlaskForm):
    u_password = PasswordField('密码',
                               render_kw={
                                   'class': 'form-control',
                                   'required': 'required'})
    ru_password = PasswordField('请再次输入密码',
                                render_kw={
                                    'class': 'form-control',
                                    'required': 'required'})
    uu_submit = SubmitField('修改',
                            render_kw={'placeholder': '修改',
                                       'class': 'btn btn-primary block full-width m-b'})
