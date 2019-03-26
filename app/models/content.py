#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-26 14:58:27
@LastEditTime: 2019-03-26 18:18:44
'''

from .. import db


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(
        db.Integer,
        db.ForeignKey('task.id', ondelete='CASCADE'),
        nullable=False)
    content = db.Column(db.String(128), nullable=False)

    def __init__(self, task_id):
        self.task_id = task_id


db.create_all()
