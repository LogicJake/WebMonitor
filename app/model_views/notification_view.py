#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:01:56
@LastEditTime: 2019-03-24 18:19:40
'''
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import ValidationError
import requests
from lxml import etree
from app.main.phantomjs import PhantomJS


class NotificationView(ModelView):
    column_labels = {
        'name': '通知方式名称',
        'type': '通知方式类型',
        'number': '邮箱/telegrame id'
    }

    form_choices = {
        'type': [('mail', '邮箱'), ('telegrame', 'telegrame')]
    }
