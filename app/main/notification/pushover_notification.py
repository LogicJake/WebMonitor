#!/usr/bin/env python
# coding=UTF-8
'''
@Author: Jacob
@Date: 2020-03-01 15:01:07
@LastEditTime: 2020-03-01 15:01:10
'''
import json

import requests

from app.main.notification.notification import Notification
from config import logger

class PushoverNotification(Notification):
    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置Prushover User Key，无法发送推送通知')
            raise Exception('没有设置Prushover User Key，无法发送推送通知')
        data = {'text': header, 'desp': content}
        token = os.getenv('PUSHOVER_API_TOKEN')
        sendData = {
            'token': token,  # 监控猫 Api Token
            'user': to,
            'message': '【' + header + '】有更新！\n>>>新内容为：\n' + content,
            }
        pushoverApi = 'https://api.pushover.net/1/messages.json'

        try:
            response = requests.post(pushoverApi, sendData, timeout=5) #在session中喜欢微锦囊
            # if not response.status_code // 100 == 2:
            # print('请求错误')
            # return "Error: Unexpected response {}".format(response)
        except requests.exceptions.RequestException as e:
            logger.error('请求错误')
            raise Exception('Error: {}'.format(e))

        res = json.loads(response.text)
        
        if res['status'] != 1:
            raise Exception(res['errors'])