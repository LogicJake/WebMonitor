#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:01:56
@LastEditTime: 2019-03-25 19:39:17
'''
import requests
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import ValidationError

from app.main.selector.selector_handler import new_handler


def check_url(form, field):
    url = form.url.data
    try:
        requests.get(url, timeout=10)
    except Exception as e:
        raise ValidationError(repr(e))


def check_selector(form, field):
    try:
        selector_type = form.selector_type.data
        selector = form.selector.data
        url = form.url.data
        is_chrome = form.is_chrome.data

        if is_chrome == 'no':
            selector_handler = new_handler('request')

            if selector_type == 'xpath':
                selector_handler.get_by_xpath(url, selector)
        else:
            selector_handler = new_handler('phantomjs')

            if selector_type == 'xpath':
                selector_handler.get_by_xpath(url, selector)
    except Exception as e:
        raise ValidationError(repr(e))


class TaskView(ModelView):
    column_labels = {
        'title': '目标名称',
        'url': '监控网址',
        'create_time': '创建时间',
        'selector_type': '元素选择器类型',
        'selector': '元素选择',
        'is_chrome': '是否使用无头浏览器',
        'frequency': '频率(分钟)',
        'last_run': '上次运行时间',
        'last_status': '上次运行结果',
        'mail': '邮件提醒',
        'telegrame': 'telegrame提醒',
        'work_status': '任务状态'
    }

    column_list = [
        'title', 'url', 'frequency', 'create_time', 'mail', 'telegrame',
        'last_run', 'last_status', 'work_status'
    ]

    form_args = {
        'url': {
            'validators': [check_url],
        },
        'selector': {
            'validators': [check_selector]
        }
    }

    form_choices = {
        'selector_type': [('xpath', 'xpath'), ('css selector',
                                               'css selector')],
        'is_chrome': [('no', 'no'), ('yes', 'yes')],
        'mail': [('yes', 'yes'), ('no', 'no')],
        'telegrame': [('no', 'no'), ('yes', 'yes')],
        'work_status': [('run', 'run'), ('stop', 'stop')]
    }

    form_excluded_columns = ('last_run', 'create_time', 'last_status')
