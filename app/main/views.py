# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 20:04:12
# @Last Modified time: 2019-03-14 21:17:03
from flask import Blueprint, redirect, render_template, request
from flask_login import login_user, logout_user
from wtforms.validators import ValidationError

from app.main.forms.login_form import LoginForm
from app.main.forms.test_from import TestForm
from app.models.user import User
from app.main.extract_info import get_content
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


@bp.route('/test', methods=['GET', 'POST'])
def test():
    error = None
    content = None
    show = False
    form = TestForm()
    if form.validate_on_submit():
        try:
            url = request.form.get('url', None)
            selector_type = request.form.get('selector_type', None)
            selector = request.form.get('selector', None)
            is_chrome = request.form.get('is_chrome', None)
            regular_expression = request.form.get('regular_expression', None)
            headers = request.form.get('headers', None)

            if is_chrome == 'yes':
                show = True
            content = get_content(url,
                                  is_chrome,
                                  selector_type,
                                  selector,
                                  regular_expression,
                                  headers,
                                  debug=True)
        except ValidationError:
            pass
        except Exception as e:
            error = repr(e)

    return render_template('test.html',
                           error=error,
                           form=form,
                           content=content,
                           show=show)
