import logging
import smtplib
import traceback
from email.header import Header
from email.mime.text import MIMEText

from setting.models import SystemMailSetting
from task.utils.notification.notification import Notification

logger = logging.getLogger('main')


class MailNotification(Notification):
    def __init__(self):
        try:
            setting = SystemMailSetting.objects.first()
        except Exception:
            logger.error('没有设置系统邮箱，无法发送邮件通知')
            logger.error(traceback.format_exc())
            raise Exception('没有设置系统邮箱，无法发送邮件通知')

        self.mail_server = setting.mail_server
        self.mail_port = setting.mail_port
        self.mail_username = setting.mail_username
        self.mail_sender = setting.mail_sender
        self.mail_password = setting.mail_password

    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置通知邮箱，无法发送邮件通知')
            raise Exception('没有设置通知邮箱，无法发送邮件通知')
        message = MIMEText(content, 'html', 'utf-8')
        message['To'] = Header(to, 'utf-8')
        message['From'] = Header('WebMonitor', 'utf-8')
        message['Subject'] = Header(header, 'utf-8')

        smtpObj = smtplib.SMTP_SSL(self.mail_server, self.mail_port)
        smtpObj.connect(self.mail_server, self.mail_port)
        smtpObj.login(self.mail_username, self.mail_password)
        smtpObj.sendmail(self.mail_sender, to, message.as_string())
