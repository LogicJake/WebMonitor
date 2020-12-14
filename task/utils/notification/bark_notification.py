
import json
import logging

import requests

from task.utils.notification.notification import Notification
import urllib.parse

logger = logging.getLogger('main')


class BarkNotification(Notification):
    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置Bark KEY，无法发送Bark通知')
            raise Exception('没有设置Bark KEY，无法发送Bark通知')
        url = 'https://api.day.app/{}/{}/{}'.format(to, header, urllib.parse.quote_plus(content))
        r = requests.post(url)

        res = json.loads(r.text)
        if res['code'] != 200:
            raise Exception(res['message'])
