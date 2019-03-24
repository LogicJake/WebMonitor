#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 20:27:55
@LastEditTime: 2019-03-24 20:46:41
'''
from app.main.notification.mail_notification import MailNotification


def new_handler(name):
    if name == 'mail':
        return MailNotification()
    elif name == 'telegrame':
        pass
    else:
        raise Exception()
