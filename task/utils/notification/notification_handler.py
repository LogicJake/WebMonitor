from task.utils.notification.mail_notification import MailNotification
from task.utils.notification.wechat_notification import WechatNotification
from task.utils.notification.pushover_notification import PushoverNotification
from task.utils.notification.bark_notification import BarkNotification
from task.utils.notification.custom_notification import CustomNotification

import logging
logger = logging.getLogger('main')


def new_handler(name):
    if name == 'mail':
        return MailNotification()
    elif name == 'wechat':
        return WechatNotification()
    elif name == 'pushover':
        return PushoverNotification()
    elif name == 'bark':
        return BarkNotification()
    elif name == 'custom':
        return CustomNotification()
    else:
        logger.error('通知方式错误')
        raise Exception('通知方式错误')
