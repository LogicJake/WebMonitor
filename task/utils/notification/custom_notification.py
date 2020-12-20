
import json
import logging

import requests

from task.utils.notification.notification import Notification
import urllib.parse

logger = logging.getLogger('main')


class CustomNotification(Notification):
    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置通知网址，无法发送自定义通知')
            raise Exception('没有设置通知网址，无法发送自定义通知')
        url = to.replace('{header}', urllib.parse.quote_plus(header)).replace('{content}', urllib.parse.quote_plus(content))
        r = requests.post(url)

        res = json.loads(r.text)
        if res['code'] != 200:
            raise Exception(res['message'])
