#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 18:03:07
@LastEditTime: 2019-03-25 18:47:02
'''
from .. import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)
    number = db.Column(db.String(64), nullable=False, default='默认')

    def __init__(self, type):
        self.type = type
