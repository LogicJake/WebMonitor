import json
import logging
import traceback

import requests
from requests.exceptions import RequestException
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

        self.token = setting.api_token

    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置Prushover User Key，无法发送推送通知')
            raise Exception('没有设置Prushover User Key，无法发送推送通知')
        token = self.token
        sendData = {
            'token': token,
            'user': to,
            'message': '【' + header + '】有更新！\n>>>新内容为：\n' + content,
        }
        pushoverApi = 'https://api.pushover.net/1/messages.json'

        try:
            response = requests.post(pushoverApi, sendData, timeout=5)
        except RequestException as e:
            logger.error('请求错误', traceback.format_exc())
            raise Exception('Error: {}'.format(e))

        res = json.loads(response.text)

        if res['status'] != 1:
            raise Exception(res['errors'])
        elif 'info' in res:
            if 'no active devices to send to' in res['info']:
                raise Exception('User key 对应的账户无激活设备，需要先行到官网购买 License')
            else:
                logger.debug(res['info'])