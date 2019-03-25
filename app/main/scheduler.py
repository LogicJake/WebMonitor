#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 14:32:34
@LastEditTime: 2019-03-25 12:15:54
'''
from datetime import datetime

import requests

from lxml import etree
from app import app, db, scheduler
from app.main.phantomjs import PhantomJS
from app.models.record import Record
from apscheduler.jobstores.base import JobLookupError


def get_content(url, is_chrome, selector_type, selector):
    if not is_chrome:
        r = requests.get(url, timeout=10)
        html = r.text

        if selector_type == 'xpath':
            s = etree.HTML(html)
            content = s.xpath(selector)

            if len(content) == 0:
                raise Exception('获取不到文本信息')
            else:
                return content[0]
    else:
        if selector_type == 'xpath':
            phantomjs = PhantomJS()
            res = phantomjs.get_by_xpath(url, selector)
            return res


def monitor(id, url, selector_type, selector, is_chrome):
    with app.app_context():
        status = None
        try:
            content = get_content(url, is_chrome, selector_type, selector)
            from app.main.notification.notification_handler import new_handler
            handler = new_handler('mail')
            handler.send('835410808@qq.com', content)
            status = '成功'
        except Exception as e:
            status = repr(e)

        record = Record.query.filter_by(id=id).first()
        record.last_run = datetime.now()
        record.last_status = status
        db.session.add(record)
        db.session.commit()


def add_job(id, url, selector_type, selector, is_chrome, interval):
    scheduler.add_job(
        func=monitor,
        args=(
            id,
            url,
            selector_type,
            selector,
            is_chrome,
        ),
        trigger='interval',
        minutes=interval,
        id='task_{}'.format(id),
        replace_existing=True)


def remove_job(id):
    try:
        scheduler.remove_job('task_{}'.format(id))
    except JobLookupError:
        pass


def pause_job(id):
    scheduler.pause_job('task_{}'.format(id))


def resume_job(id):
    scheduler.resume_job('task_{}'.format(id))
