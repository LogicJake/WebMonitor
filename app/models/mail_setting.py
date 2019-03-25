#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 18:29:53
@LastEditTime: 2019-03-25 11:10:18
'''
from .. import db


class MailSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail_server = db.Column(db.String(32), nullable=False, default='localhost')
    mail_port = db.Column(db.Integer, nullable=False, default=25)
    mail_username = db.Column(db.String(64), nullable=False, default='默认用户名')
    mail_sender = db.Column(
        db.String(64), nullable=False, default='默认用户名@mail.com')
    mail_password = db.Column(db.String(64), nullable=False, default='默认密码')
