import logging
import traceback

from setting.models import SlackSetting
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from task.utils.notification.notification import Notification

logger = logging.getLogger('main')


class SlackNotification(Notification):
    def __init__(self):
        try:
            setting = SlackSetting.objects.first()
        except Exception:
            logger.error('没有设置 Slack OAuth Access Token，无法发送通知')
            logger.error(traceback.format_exc())
            raise Exception('没有设置 Slack OAuth Access Token，无法发送通知')

        self.token = setting.token

    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置 channel 名称，无法发送 Slack 通知')
            raise Exception('没有设置 channel 名称，无法发送 Slack 通知')
        client = WebClient(token=self.token)

        try:
            client.chat_postMessage(channel=to,
                                    text='{}:{}'.format(header, content))
        except SlackApiError as e:
            raise Exception(e.response['error'])
