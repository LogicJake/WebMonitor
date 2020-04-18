
import json
import logging

import requests

from task.utils.notification.notification import Notification

logger = logging.getLogger('main')


class WechatNotification(Notification):
    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置Server酱 SCKEY，无法发送微信通知')
            raise Exception('没有设置Server酱 SCKEY，无法发送微信通知')
        data = {'text': header, 'desp': content}
        url = 'https://sc.ftqq.com/{}.send'.format(to)
        r = requests.post(url, data=data)

        res = json.loads(r.text)
        if res['errno'] != 0:
            raise Exception(res['errmsg'])
