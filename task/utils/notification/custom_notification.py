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
        loc = to.find("{data=")
        if loc == -1:
            url = to.replace('{header}',
                             urllib.parse.quote_plus(header)).replace(
                                 '{content}', urllib.parse.quote_plus(content))
            r = requests.get(url)
            res = json.loads(r.text)
            logger.debug('自定义[GET]通知：{}，结果：{}'.format(url, res))

        else:
            url = to[:loc]
            data = to[loc + 6:to.rfind("}")].replace(
                '{header}',
                json.dumps(header)).replace('{content}', json.dumps(content))
            r = requests.post(url, json=json.loads(data))
            res = json.loads(r.text)
            logger.debug('自定义[POST]通知：{}，传输数据：{}，结果：{}'.format(url, data, res))
