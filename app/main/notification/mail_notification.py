#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 20:23:33
@LastEditTime: 2019-03-31 22:01:44
'''
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from app import db
from app.main.notification.notification import Notification
from app.models.mail_setting import MailSetting
from config import logger


class MailNotification(Notification):
    def __init__(self):
        setting = db.session.query(MailSetting).first()
        if setting.mail_sender != '默认用户名@mail.com':
            self.mail_server = setting.mail_server
            self.mail_port = setting.mail_port
            self.mail_username = setting.mail_username
            self.mail_sender = setting.mail_sender
            self.mail_password = setting.mail_password
        else:
            logger.error('没有设置系统邮箱，无法发送邮件通知')
            raise Exception('没有设置系统邮箱，无法发送邮件通知')

    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置通知邮箱，无法发送邮件通知')
            raise Exception('没有设置通知邮箱，无法发送邮件通知')
        message = MIMEText(content, 'html', 'utf-8')
        message['To'] = Header(to, 'utf-8')
        message['From'] = Header('WebMonitor', 'utf-8')
        message['Subject'] = Header(header, 'utf-8')

        smtpObj = smtplib.SMTP()
        smtpObj.connect(self.mail_server, self.mail_port)
        smtpObj.login(self.mail_username, self.mail_password)
        smtpObj.sendmail(self.mail_sender, to, message.as_string())
