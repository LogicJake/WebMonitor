#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 16:35:24
@LastEditTime: 2019-03-25 18:29:02
'''
from .. import db
from datetime import datetime
from sqlalchemy import event


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    url = db.Column(db.String(64), nullable=False)
    selector_type = db.Column(db.String(64), nullable=False)
    selector = db.Column(db.String(64), nullable=False)
    is_chrome = db.Column(db.String(64), nullable=False, default='no')
    frequency = db.Column(db.Integer, nullable=False, default='5')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_run = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_status = db.Column(db.String(64), nullable=False, default='创建任务成功')
    # 通知方式
    mail = db.Column(db.String(32), nullable=False, default='yes')
    telegrame = db.Column(db.String(32), nullable=False, default='no')


def after_insert_listener(mapper, connection, target):
    from app.main.scheduler import add_job

    add_job(target.id, target.url, target.selector_type, target.selector,
            target.is_chrome, target.frequency)


def after_update_listener(mapper, connection, target):
    from app.main.scheduler import add_job

    add_job(target.id, target.url, target.selector_type, target.selector,
            target.is_chrome, target.frequency)


def after_delete_listener(mapper, connection, target):
    from app.main.scheduler import remove_job
    id = target.id

    remove_job(id)


event.listen(Record, 'after_insert', after_insert_listener)
event.listen(Record, 'after_update', after_update_listener)
event.listen(Record, 'after_delete', after_delete_listener)
