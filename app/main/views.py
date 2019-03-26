# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 20:04:12
# @Last Modified time: 2019-03-14 21:17:03
from flask import Blueprint, render_template, request, redirect
from app.main.notification.notification_handler import new_handler
from flask_login import login_user, logout_user
from app.models.user import User
from app.main.login_form import LoginForm

bp = Blueprint('main', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User.query.filter_by(name=user_name).first()
        if user and password and user.password == password:
            login_user(user, remember=remember_me)
            return redirect('/')
        else:
            error = '账户名或密码错误'
    return render_template('login.html', error=error, form=form)


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return '注销成功'
