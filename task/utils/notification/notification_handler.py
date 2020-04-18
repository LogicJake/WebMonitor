from task.utils.notification.mail_notification import MailNotification
from task.utils.notification.wechat_notification import WechatNotification
from task.utils.notification.pushover_notification import PushoverNotification

import logging
logger = logging.getLogger('main')


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
