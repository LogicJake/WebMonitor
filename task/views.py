from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
import logging

logger = logging.getLogger('main')


def ping():
    logger.info('pong!!')


# 定时器
scheduler = BackgroundScheduler()
scheduler.configure(timezone='Asia/Shanghai')
scheduler.add_jobstore(DjangoJobStore(), 'default')
scheduler.add_job(func=ping,
                  trigger='interval',
                  minutes=1,
                  id='ping',
                  replace_existing=True)
register_events(scheduler)
scheduler.start()
