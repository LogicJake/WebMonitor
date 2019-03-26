# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 19:33:23
# @Last Modified time: 2019-03-13 17:06:37
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from app.model_views.task_view import TaskView
from app.model_views.notification_view import NotificationView
from app.model_views.mail_setting_view import MailSettingView
from app.model_views.task_status_view import TaskStatusView
from app.model_views.user_view import UserView

from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap

import psutil
import os

db = SQLAlchemy()
login = LoginManager()
admin = Admin(name='I AM WATCHING YOU', template_mode='bootstrap3')
scheduler = APScheduler()
app = Flask(__name__)
bootstrap = Bootstrap()


def create_app(config_name):
    from config import config
    app.config.from_object(config[config_name])

    # 注册flask-login
    login.init_app(app)

    # bootstrap
    bootstrap.init_app(app)

    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # 注册蓝图
    from app.main.views import bp as main_bp
    app.register_blueprint(main_bp)

    # 注册数据库
    db.init_app(app)

    # 注册flask-admin
    admin.init_app(
        app,
        index_view=AdminIndexView(
            name='导航栏', template='admin/index.html', url='/'))

    # 注册APScheduler
    scheduler.init_app(app)
    scheduler.start()

    # 视图
    from app.models.task import Task
    from app.models.mail_setting import MailSetting
    from app.models.notification import Notification
    from app.models.task_status import TaskStatus
    from app.models.user import User

    admin.add_view(TaskStatusView(TaskStatus, db.session, name='任务状态'))
    admin.add_view(TaskView(Task, db.session, name='任务管理'))
    admin.add_view(NotificationView(Notification, db.session, name='通知方式管理'))
    admin.add_view(MailSettingView(MailSetting, db.session, name='系统邮箱设置'))
    admin.add_view(UserView(User, db.session, name='账号密码管理'))

    with app.test_request_context():
        db.create_all()
        mail_setting = MailSetting.query.first()
        # 插入默认邮箱配置
        if mail_setting is None:
            mail_setting = MailSetting()
            db.session.add(mail_setting)
            db.session.commit()

        # 初始化账号密码
        user = User.query.first()
        if user is None:
            import random
            import string
            random_password = ''.join(
                random.sample(string.ascii_letters + string.digits, 10))

            user = User('admin', random_password)
            db.session.add(user)
            db.session.commit()

        # 插入默认通知方式
        notis = Notification.query.all()
        mail_exist = False
        wechat_exist = False

        if len(notis) != 0:
            for noti in notis:
                if noti.type == 'mail':
                    mail_exist = True
                if noti.type == 'wechat':
                    wechat_exist = True

        if not mail_exist:
            mail_noti = Notification('mail')
            db.session.add(mail_noti)
            db.session.commit()
        if not wechat_exist:
            wechat_noti = Notification('wechat')
            db.session.add(wechat_noti)
            db.session.commit()

        ppid = psutil.Process(os.getppid())
        ppid_name = ppid.name()
        # 加这一步判断主要是因为，
        # 在debug模式下，会启动另外一个线程来自动重载，
        # 这样会导致在两个线程中都启动任务，造成重复
        if 'python' not in ppid_name:
            # 在系统重启时重启任务
            from app.main.scheduler import add_job
            task_statuss = TaskStatus.query.all()
            for task_status in task_statuss:
                if task_status.task_status == 'run':
                    task_id = task_status.task_id
                    task = Task.query.filter_by(id=task_id).first()
                    add_job(task.id, task.frequency)
    return app
