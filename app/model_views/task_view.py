#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:01:56
@LastEditTime: 2019-03-30 11:04:21
'''
import requests
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import ValidationError
from flask_login import current_user
from app.main.selector.selector_handler import new_handler
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


def check_selector(form, field):
    try:
        selector_type = form.selector_type.data
        selector = form.selector.data
        url = form.url.data
        is_chrome = form.is_chrome.data
        headers = form.headers.data

        if is_chrome == 'no':
            selector_handler = new_handler('request')
        else:
            selector_handler = new_handler('phantomjs')

        if selector_type == 'xpath':
            selector_handler.get_by_xpath(url, selector, headers)
        elif selector_type == 'css':
            selector_handler.get_by_css(url, selector, headers)
        else:
            raise Exception('无效选择器')
    except Exception as e:
        raise ValidationError(repr(e))


class TaskView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    column_labels = {
        'id': '任务id',
        'name': '任务名称',
        'url': '监控网址',
        'create_time': '创建时间',
        'selector_type': '元素选择器类型',
        'selector': '元素选择',
        'is_chrome': '是否使用无头浏览器',
        'frequency': '频率(分钟)',
        'mail': '邮件提醒',
        'wechat': '微信提醒',
        'regular_expression': '正则表达式',
        'rule': '监控规则',
        'headers': '自定义请求头'
    }

    column_descriptions = {
        'regular_expression': '使用正则表达式进一步提取信息，可以留空',
        'rule': '规则写法参考<a href="www.github.com">文档</a>，留空则只简单监控内容变化',
        'headers': '自定义请求头，如可以设置cookie获取登录后才能查看的页面'
    }

    column_list = [
        'id', 'name', 'url', 'frequency', 'create_time', 'mail', 'wechat'
    ]

    form_args = {
        'url': {
            'validators': [check_url],
        },
        'selector': {
            'validators': [check_selector]
        },
        'wechat': {
            'validators': [check_noti]
        }
    }

    form_choices = {
        'selector_type': [('xpath', 'xpath'), ('css', 'css selector')],
        'is_chrome': [('no', 'no'), ('yes', 'yes')],
        'mail': [('no', 'no'), ('yes', 'yes')],
        'wechat': [('no', 'no'), ('yes', 'yes')],
    }

    form_excluded_columns = ('create_time')
