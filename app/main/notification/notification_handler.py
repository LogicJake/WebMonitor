#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 20:27:55
@LastEditTime: 2019-03-26 21:32:18
'''
from app.main.notification.mail_notification import MailNotification
from app.main.notification.wechat_notification import WechatNotification
from config import logger


def new_handler(name):
    if name == 'mail':
        return MailNotification()
    elif name == 'wechat':
        return WechatNotification()
    else:
        logger.error('通知方式错误')
        raise Exception('通知方式错误')
