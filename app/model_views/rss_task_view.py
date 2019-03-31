#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:01:56
@LastEditTime: 2019-03-31 20:50:38
'''
import requests
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import ValidationError
from flask_login import current_user
from flask import redirect, url_for


def check_url(form, field):
    url = form.url.data
    try:
        requests.get(url, timeout=10)
    except Exception as e:
        raise ValidationError(repr(e))


def check_noti(form, field):
    is_wechat = form.wechat.data
    is_mail = form.mail.data

    if is_wechat == 'no' and is_mail == 'no':
        raise ValidationError('必须选择一个通知方式')


class RSSTaskView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    column_labels = {
        'id': '任务id',
        'name': '任务名称',
        'url': 'RSS地址',
        'create_time': '创建时间',
        'frequency': '频率(分钟)',
        'mail': '邮件提醒',
        'wechat': '微信提醒',
    }

    column_list = [
        'id', 'name', 'url', 'frequency', 'create_time', 'mail', 'wechat'
    ]

    form_args = {
        'url': {
            'validators': [check_url],
        },
        'wechat': {
            'validators': [check_noti]
        }
    }

    form_choices = {
        'mail': [('no', 'no'), ('yes', 'yes')],
        'wechat': [('no', 'no'), ('yes', 'yes')],
    }

    form_excluded_columns = ('create_time')
