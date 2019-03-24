#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 18:03:07
@LastEditTime: 2019-03-24 18:17:07
'''
from .. import db
from datetime import datetime
from sqlalchemy import event


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    type = db.Column(db.String(64), nullable=False, default='mail')
    number = db.Column(db.String(64), nullable=False)
