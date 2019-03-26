#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 16:35:24
@LastEditTime: 2019-03-26 10:08:56
'''
from .. import db
from datetime import datetime
from sqlalchemy import event


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    url = db.Column(db.String(128), nullable=False)
    selector_type = db.Column(db.String(32), nullable=False, default='xpath')
    selector = db.Column(db.String(128), nullable=False)
    is_chrome = db.Column(db.String(32), nullable=False, default='no')
    frequency = db.Column(db.Integer, nullable=False, default='5')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # 通知方式
    mail = db.Column(db.String(32), nullable=False, default='yes')
    wechat = db.Column(db.String(32), nullable=False, default='no')


def after_insert_listener(mapper, connection, target):
    from app.main.scheduler import add_job

    add_job(target.id, target.url, target.selector_type, target.selector,
            target.is_chrome, target.frequency)

    from app.models.task_status import TaskStatus
    task_status = TaskStatus.__table__
    connection.execute(task_status.insert().values(
        task_id=target.id, task_name=target.name))


def after_update_listener(mapper, connection, target):
    from app.main.scheduler import add_job, remove_job

    remove_job(target.id)

    add_job(target.id, target.url, target.selector_type, target.selector,
            target.is_chrome, target.frequency)


def after_delete_listener(mapper, connection, target):
    from app.main.scheduler import remove_job

    remove_job(target.id)

    from app.models.task_status import TaskStatus
    task_status = TaskStatus.__table__
    connection.execute(
        task_status.delete().where(TaskStatus.task_id == target.id))


event.listen(Task, 'after_insert', after_insert_listener)
event.listen(Task, 'after_update', after_update_listener)
event.listen(Task, 'after_delete', after_delete_listener)
