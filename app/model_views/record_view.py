#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:01:56
@LastEditTime: 2019-03-24 17:25:31
'''
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import ValidationError
import requests
from lxml import etree
from app.main.phantomjs import PhantomJS


def check_url(form, field):
    url = form.url.data
    try:
        requests.get(url, timeout=10)
    except Exception as e:
        raise ValidationError(str(e))


def check_selector(form, field):
    selector_type = form.selector_type.data
    selector = form.selector.data
    url = form.url.data
    is_chrome = form.is_chrome.data

    if not is_chrome:
        r = requests.get(url, timeout=10)
        html = r.text

        if selector_type == 'xpath':
            s = etree.HTML(html)
            content = s.xpath(selector)

            if len(content) == 0:
                raise ValidationError('获取不到文本信息，可以尝试选择使用无头浏览器再试一次')
    else:
        if selector_type == 'xpath':
            phantomjs = PhantomJS()
            res = phantomjs.get_by_xpath(url, selector)
            if res is None:
                raise ValidationError('获取不到文本信息，请确保xpath语句正确')


class RecordView(ModelView):
    column_labels = {
        'title': '目标名称',
        'url': '监控网址',
        'create_time': '创建时间',
        'selector_type': '元素选择器类型',
        'selector': '元素选择',
        'is_chrome': '是否使用无头浏览器',
        'frequency': '频率(分钟)',
        'last_run': '上次运行时间'
    }
    column_list = ['title', 'url',  'frequency', 'create_time', 'last_run']

    form_args = dict(
        url=dict(validators=[check_url]),
        selector=dict(validators=[check_selector]))

    form_choices = {
        'selector_type': [('xpath', 'xpath'), ('css selector',
                                               'css selector')],
        'is_chrome': [('no', 'no'), ('yes', 'yes')]
    }

    form_excluded_columns = ('last_run', 'create_time')

    form_widget_args = {
        'last_run': {
            'readonly': True
        },
        'create_time': {
            'readonly': True
        },
    }
