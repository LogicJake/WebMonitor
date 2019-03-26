#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 20:27:55
@LastEditTime: 2019-03-26 10:00:54
'''
from app.main.notification.mail_notification import MailNotification
from app.main.notification.wechat_notification import WechatNotification


def new_handler(name):
    if name == 'mail':
        return MailNotification()
    elif name == 'wechat':
        return WechatNotification()
    else:
        raise Exception('通知方式错误')
