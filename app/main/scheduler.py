#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 14:32:34
@LastEditTime: 2019-03-26 17:31:42
'''
from datetime import datetime

from apscheduler.jobstores.base import JobLookupError

from app import app, db, scheduler
from app.models.notification import Notification
from app.models.task import Task
from app.models.content import Content
from app.models.task_status import TaskStatus
from app.main.extract_info import get_content
from app.main.rule import is_changed


def wraper_msg(title, content):
    header = title
    content = content
    return header, content


def send_message(content, name, mail, wechat):
    from app.main.notification.notification_handler import new_handler

    header, content = wraper_msg(name, content)

    if mail == 'yes':
        handler = new_handler('mail')
        mail_info = Notification.query.filter_by(type='mail').first()
        mail_address = mail_info.number
        handler.send(mail_address, header, content)

    if wechat == 'yes':
        handler = new_handler('wechat')
        wechat_info = Notification.query.filter_by(type='wechat').first()
        key = wechat_info.number
        handler.send(key, header, content)


def monitor(id):
    with app.app_context():
        status = '成功执行但未监测到变化'
        try:
            task = Task.query.filter_by(id=id).first()
            url = task.url
            selector_type = task.selector_type
            selector = task.selector
            is_chrome = task.is_chrome
            regular_expression = task.regular_expression
            mail = task.mail
            wechat = task.wechat
            name = task.name
            rule = task.rule

            last = Content.query.filter_by(task_id=id).first()
            if not last:
                last = Content(id)

            last_content = last.content
            content = get_content(url, is_chrome, selector_type, selector,
                                  regular_expression)
            if is_changed(rule, content, last_content):
                send_message(content, name, mail, wechat)
                last.content = content
                db.session.add(last)
                db.session.commit()
                status = '监测到变化，最新值：' + content
        except Exception as e:
            status = repr(e)

        task_status = TaskStatus.query.filter_by(id=id).first()
        task_status.last_run = datetime.now()
        task_status.last_status = status
        db.session.add(task_status)
        db.session.commit()


def add_job(id, interval):
    scheduler.add_job(
        func=monitor,
        args=(id, ),
        trigger='interval',
        minutes=interval,
        id='task_{}'.format(id),
        replace_existing=True)


def remove_job(id):
    try:
        scheduler.remove_job('task_{}'.format(id))
    except JobLookupError:
        pass
