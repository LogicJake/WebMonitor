#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-26 14:58:27
@LastEditTime: 2019-03-31 19:10:01
'''

from .. import db


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(512), nullable=False)
    task_type = db.Column(db.String(32), nullable=False, default='html')

    def __init__(self, task_id, task_type='html'):
        self.task_id = task_id
        self.task_type = task_type


db.create_all()
