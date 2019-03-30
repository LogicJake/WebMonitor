from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired("请输入帐号!")])
    password = PasswordField('密码', validators=[DataRequired("请输入密码!")])
    remember_me = BooleanField('记住我', default=False)
    submit = SubmitField('登录')
