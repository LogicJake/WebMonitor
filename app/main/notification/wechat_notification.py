#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 20:23:33
@LastEditTime: 2019-03-26 09:57:26
'''
import requests
from app.main.notification.notification import Notification
import json


class WechatNotification(Notification):
    def send(self, to, header, content):
        if to == '默认':
            raise Exception('没有设置Server酱 SCKEY，无法发送微信通知')
        data = {'text': header, 'desp': content}
        url = 'https://sc.ftqq.com/{}.send'.format(to)
        r = requests.post(url, data=data)

        res = json.loads(r.text)
        if res['errno'] != 0:
            raise Exception(res['errmsg'])
