#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 14:32:34
@LastEditTime: 2019-03-24 17:23:57
'''
from datetime import datetime

from app import scheduler, app, db
from app.models.record import Record
from apscheduler.jobstores.base import JobLookupError


def monitor(id):
    with app.app_context():
        record = Record.query.filter_by(id=id).first()
        record.last_run = datetime.now()
        db.session.add(record)
        db.session.commit()


def add_job(id, interval):
    scheduler.add_job(func=monitor,
                      args=(id,),
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
