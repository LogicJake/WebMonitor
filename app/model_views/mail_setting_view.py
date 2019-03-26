#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 18:41:42
@LastEditTime: 2019-03-26 20:51:52
'''
from flask_login import current_user
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView


class MailSettingView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    column_labels = {
        'mail_server': '邮箱服务器',
        'mail_port': '端口',
        'mail_username': '用户名',
        'mail_password': '密码',
        'mail_sender': '发件人'
    }

    can_create = False
    can_delete = False

    column_descriptions = {'mail_sender': '一般为邮箱地址', 'mail_password': '授权码'}
