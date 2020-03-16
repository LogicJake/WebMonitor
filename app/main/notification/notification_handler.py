#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake, Jacob
@Date: 2019-03-24 20:27:55
@LastEditTime: 2020-03-01 15:00:54
'''
from app.main.notification.mail_notification import MailNotification
from app.main.notification.wechat_notification import WechatNotification
from app.main.notification.pushover_notification import PushoverNotification
from config import logger


def new_handler(name):
    if name == 'mail':
        return MailNotification()
    elif name == 'wechat':
        return WechatNotification()
    elif name == 'pushover':
        return PushoverNotification()
    else:
        logger.error('通知方式错误')
        raise Exception('通知方式错误')
