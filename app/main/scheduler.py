#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 14:32:34
@LastEditTime: 2020-03-16 13:41:46
'''
import traceback
from datetime import datetime

import markdown
from apscheduler.jobstores.base import JobLookupError
from func_timeout.exceptions import FunctionTimedOut

from app import app, db, scheduler
from app.main.extract_info import get_content, get_rss_content
from app.main.rule import is_changed
from app.models.content import Content
from app.models.notification import Notification
from app.models.rss_task import RSSTask
from app.models.task import Task
from app.models.task_status import TaskStatus
from config import logger


# 部分通知方式出错异常
class PartNotificationError(Exception):
    pass


def wraper_rss_msg(item):
    title = item['title']
    link = item['link']

    res = '''[{}]({})'''.format(title, link)
    return res


def wraper_msg(content, link):
    res = '''[{}]({})'''.format(content, link)
    return res


def send_message(content, header, mail, wechat, pushover):
    from app.main.notification.notification_handler import new_handler

    total = 0
    fail = 0

    exception_content = ''
    try:
        if mail == 'yes':
            total += 1
            handler = new_handler('mail')
            mail_info = Notification.query.filter_by(type='mail').first()
            mail_address = mail_info.number
            content = markdown.markdown(content,
                                        output_format='html5',
                                        extensions=['extra'])
            handler.send(mail_address, header, content)
    except Exception as e:
        fail += 1
        exception_content += 'Mail Exception: {};'.format(repr(e))

    try:
        if wechat == 'yes':
            total += 1
            handler = new_handler('wechat')
            wechat_info = Notification.query.filter_by(type='wechat').first()
            key = wechat_info.number
            handler.send(key, header, content)
    except Exception as e:
        fail += 1
        exception_content += 'Wechat Exception: {};'.format(repr(e))

    try:
        if pushover == 'yes':
            total += 1
            handler = new_handler('pushover')
            pushover_info = Notification.query.filter_by(
                type='pushover').first()
            key = pushover_info.number
            handler.send(key, header, content)
    except Exception as e:
        fail += 1
        exception_content += 'Pushover Exception: {};'.format(repr(e))

    if fail > 0:
        if fail < total:
            raise PartNotificationError(exception_content)
        else:
            raise Exception(exception_content)


def monitor(id, type):
    with app.app_context():
        status = '成功执行但未监测到变化'
        global_content = None
        try:
            if type == 'html':
                task = Task.query.filter_by(id=id).first()
                url = task.url
                selector_type = task.selector_type
                selector = task.selector
                is_chrome = task.is_chrome
                regular_expression = task.regular_expression
                mail = task.mail
                wechat = task.wechat
                pushover = task.pushover
                name = task.name
                rule = task.rule
                headers = task.headers

                last = Content.query.filter_by(task_id=id,
                                               task_type=type).first()
                if not last:
                    last = Content(id)

                last_content = last.content
                content = get_content(url, is_chrome, selector_type, selector,
                                      regular_expression, headers)
                global_content = content
                status_code = is_changed(rule, content, last_content)
                logger.info(
                    'rule: {}, content: {}, last_content: {}, status_code: {}'.
                    format(rule, content, last_content, status_code))
                if status_code == 1:
                    status = '监测到变化，但未命中规则，最新值为{}'.format(content)
                    last.content = content
                    db.session.add(last)
                    db.session.commit()
                elif status_code == 2:
                    status = '监测到变化，且命中规则，最新值为{}'.format(content)
                    msg = wraper_msg(content, url)
                    send_message(msg, name, mail, wechat, pushover)
                    last.content = content
                    db.session.add(last)
                    db.session.commit()
                elif status_code == 3:
                    status = '监测到变化，最新值为{}'.format(content)
                    msg = wraper_msg(content, url)
                    send_message(msg, name, mail, wechat, pushover)
                    last.content = content
                    db.session.add(last)
                    db.session.commit()
            elif type == 'rss':
                rss_task = RSSTask.query.filter_by(id=id).first()
                url = rss_task.url
                name = rss_task.name
                mail = rss_task.mail
                wechat = rss_task.wechat
                pushover = rss_task.pushover

                last = Content.query.filter_by(task_id=id,
                                               task_type=type).first()
                if not last:
                    last = Content(id, 'rss')

                last_guid = last.content
                item = get_rss_content(url)
                if item['guid'] != last_guid:
                    global_content = content
                    content = wraper_rss_msg(item)
                    send_message(content, name, mail, wechat, pushover)
                    last.content = item['guid']
                    db.session.add(last)
                    db.session.commit()
                    status = '监测到变化，最新值：' + item['title']

        except FunctionTimedOut:
            logger.error(traceback.format_exc())
            status = '解析RSS超时'
        except PartNotificationError as e:
            logger.error(traceback.format_exc())
            status = repr(e)
            last.content = global_content
            db.session.add(last)
            db.session.commit()
        except Exception as e:
            logger.error(traceback.format_exc())
            status = repr(e)

        task_status = TaskStatus.query.filter_by(task_id=id,
                                                 task_type=type).first()
        task_status.last_run = datetime.now()
        task_status.last_status = status
        db.session.add(task_status)
        db.session.commit()


def add_job(id, interval, type='html'):
    if type == 'html':
        task_id = id
    elif type == 'rss':
        task_id = 'rss{}'.format(id)

    scheduler.add_job(func=monitor,
                      args=(
                          id,
                          type,
                      ),
                      trigger='interval',
                      minutes=interval,
                      id='task_{}'.format(task_id),
                      replace_existing=True)
    logger.info('添加task_{}'.format(task_id))


def remove_job(id, type='html'):
    if type == 'html':
        task_id = id
    elif type == 'rss':
        task_id = 'rss{}'.format(id)

    try:
        scheduler.remove_job('task_{}'.format(task_id))
        logger.info('删除task_{}'.format(task_id))
    except JobLookupError as e:
        logger.info(e)
        logger.info('task_{}不存在'.format(task_id))
