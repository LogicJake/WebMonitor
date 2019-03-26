#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 20:23:33
@LastEditTime: 2019-03-26 21:32:59
'''
import json

import requests

from app.main.notification.notification import Notification
from config import logger


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
