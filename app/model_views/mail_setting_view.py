#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 18:41:42
@LastEditTime: 2019-03-25 11:10:04
'''

from flask_admin.contrib.sqla import ModelView


class MailSettingView(ModelView):
    column_labels = {
        'mail_server': '邮箱服务器',
        'mail_port': '端口',
        'mail_username': '用户名',
        'mail_password': '密码',
        'mail_sender': '发送人邮箱'
    }

    can_create = False
    can_edit = True
    can_delete = False

    column_descriptions = {'mail_sender': '一般为邮箱地址', 'mail_password': '授权码'}
