from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, ValidationError

from apps.user.model import User


class UserRegisterForm(FlaskForm):
    username=StringField(validators=[DataRequired(message='该数据必须填写'),Length(max=20,message='用户名称不能多于20位')])
    password=StringField(validators=[DataRequired(message='密码必须填写')])
    repassword=StringField(validators=[DataRequired(message='密码必须填写'),EqualTo('password',message='两次密码输入不一致')])
    phone=StringField(validators=[DataRequired(message='电话必须填写'),Length(max=11,message='不能超过11位'),Regexp(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$',message='手机号码格式错误')])
    email=StringField(validators=[Regexp(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',message='邮箱格式错误')])

class LoginForm(FlaskForm):
    phone=StringField()
    password=StringField()

class AddUserForm(FlaskForm):
    username = StringField(validators=[DataRequired(message='该数据必须填写'), Length(max=20, message='用户名称不能多于20位')])
    password = StringField(validators=[DataRequired(message='密码必须填写')])
    phone = StringField(validators=[DataRequired(message='电话必须填写'), Length(max=11, message='不能超过11位'), Regexp(
        r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$', message='手机号码格式错误')])
    email = StringField(validators=[Regexp(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', message='邮箱格式错误')])

    def validate_phone(self,data):
        user=User.query.filter(User.phone==data.data).first()
        if user:
            raise ValidationError('手机号码已注册')

class ModifyUserForm(FlaskForm):
    user_id=IntegerField(validators=[DataRequired(message='该数据必须填写')])
    username = StringField(validators=[DataRequired(message='该数据必须填写'), Length(max=20, message='用户名称不能多于20位')])
    password = StringField(validators=[DataRequired(message='密码必须填写')])
    phone = StringField(validators=[DataRequired(message='电话必须填写'), Length(max=11, message='不能超过11位'), Regexp(
        r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$', message='手机号码格式错误')])
    email = StringField(validators=[Regexp(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', message='邮箱格式错误')])