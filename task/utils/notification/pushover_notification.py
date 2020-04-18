import json
import logging
import os
import traceback

import requests

from setting.models import PushoverSetting
from task.utils.notification.notification import Notification

logger = logging.getLogger('main')


class PushoverNotification(Notification):
    def __init__(self):
        try:
            setting = PushoverSetting.objects.first()
        except Exception:
            logger.error('没有设置Pushover API Token，无法发送通知')
            logger.error(traceback.format_exc())
            raise Exception('没有设置Pushover API Token，无法发送通知')

        self.token = setting.token

    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置Prushover User Key，无法发送推送通知')
            raise Exception('没有设置Prushover User Key，无法发送推送通知')
        token = self.token
        sendData = {
            'token': token,  # 监控猫 Api Token
            'user': to,
            'message': '【' + header + '】有更新！\n>>>新内容为：\n' + content,
        }
        pushoverApi = 'https://api.pushover.net/1/messages.json'

        try:
            response = requests.post(pushoverApi, sendData, timeout=5)
        except requests.exceptions.RequestException as e:
            logger.error('请求错误')
            raise Exception('Error: {}'.format(e))

        res = json.loads(response.text)

        if res['status'] != 1:
            raise Exception(res['errors'])
