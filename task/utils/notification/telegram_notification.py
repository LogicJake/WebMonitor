import logging
import traceback
import urllib.parse

import requests
from setting.models import TelegramSetting
from task.utils.notification.notification import Notification

logger = logging.getLogger('main')


class TelegramNotification(Notification):
    def __init__(self):
        try:
            setting = TelegramSetting.objects.first()
        except Exception:
            logger.error('没有设置 Telegram bot token，无法发送通知')
            logger.error(traceback.format_exc())
            raise Exception('没有设置 Telegram bot token，无法发送通知')

        self.token = setting.token

    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置 chat_id，无法发送 Telegram 通知')
            raise Exception('没有设置 chat_id，无法发送 Telegram 通知')

        r = requests.get(
            'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.
            format(self.token, to,
                   urllib.parse.quote_plus('{}: {}'.format(header, content))))
        result = r.json()
        if not result['ok']:
            raise Exception(result['description'])
