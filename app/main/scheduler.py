#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 14:32:34
@LastEditTime: 2019-03-25 13:25:32
'''
from datetime import datetime

from apscheduler.jobstores.base import JobLookupError

from app import app, db, scheduler
from app.main.selector.selector_handler import new_handler
from app.models.record import Record


def get_content(url, is_chrome, selector_type, selector):
    if is_chrome == 'no':
        selector_handler = new_handler('request')

        if selector_type == 'xpath':
            return selector_handler.get_by_xpath(url, selector)
    else:
        selector_handler = new_handler('phantomjs')

        if selector_type == 'xpath':
            return selector_handler.get_by_xpath(url, selector)


def monitor(id, url, selector_type, selector, is_chrome):
    with app.app_context():
        status = '成功'
        try:
            content = get_content(url, is_chrome, selector_type, selector)
            from app.main.notification.notification_handler import new_handler
            handler = new_handler('mail')
            handler.send('835410808@qq.com', content)
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
