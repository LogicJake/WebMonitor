#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:01:56
@LastEditTime: 2019-03-25 18:50:58
'''
from flask_admin.contrib.sqla import ModelView


class NotificationView(ModelView):
    can_create = False
    can_delete = False

    column_labels = {'type': '通知方式', 'number': '邮箱地址/telegrame id'}

    form_widget_args = {'type': {'readonly': True}}
