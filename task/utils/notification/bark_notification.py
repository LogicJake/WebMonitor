import json
import logging
import re
import requests

from task.utils.notification.notification import Notification
import urllib.parse

logger = logging.getLogger('main')


def getUrlQuery(content):
    """
    Extract the first URL in the content with format of '?url=URL', return '' if none URL found.
    """
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = re.findall(regex, content)
    if len(urls):
        url = [x[0] for x in urls][0]
        url_query = f'?url={urllib.parse.quote_plus(url)}'
        return url_query
    return ''


class BarkNotification(Notification):
    def send(self, to, header, content):
        if to == '默认':
            logger.error('没有设置Bark KEY，无法发送Bark通知')
            raise Exception('没有设置Bark KEY，无法发送Bark通知')
        url = 'https://api.day.app/{}/{}/{}{}'.format(
            to, header, urllib.parse.quote_plus(content), getUrlQuery(content))
        r = requests.post(url)

        res = json.loads(r.text)
        if res['code'] != 200:
            raise Exception(res['message'])
