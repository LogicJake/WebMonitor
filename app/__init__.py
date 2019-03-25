# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 19:33:23
# @Last Modified time: 2019-03-13 17:06:37
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from app.model_views.record_view import RecordView
from app.model_views.notification_view import NotificationView
from app.model_views.mail_setting_view import MailSettingView

from flask_apscheduler import APScheduler

db = SQLAlchemy()
admin = Admin(name='I AM WATCHING YOU', template_mode='bootstrap3')
scheduler = APScheduler()
app = Flask(__name__)


def create_app(config_name):
    from config import config
    app.config.from_object(config[config_name])

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
    from app.models.record import Record
    from app.models.mail_setting import MailSetting
    from app.models.notification import Notification

    admin.add_view(RecordView(Record, db.session, name='监控管理'))
    admin.add_view(NotificationView(Notification, db.session, name='通知方式管理'))
    admin.add_view(MailSettingView(MailSetting, db.session, name='系统邮箱设置'))

    with app.test_request_context():
        db.create_all()
        mail_setting = MailSetting.query.first()
        # 插入默认邮箱配置
        if mail_setting is None:
            mail_setting = MailSetting()
            db.session.add(mail_setting)
            db.session.commit()

        notis = Notification.query.all()
        mail_exist = False
        telegrame_exist = False

        if len(notis) != 0:
            for noti in notis:
                if noti.type == 'mail':
                    mail_exist = True
                if noti.type == 'telegrame':
                    telegrame_exist = True

        if not mail_exist:
            mail_noti = Notification('mail')
            db.session.add(mail_noti)
            db.session.commit()
        if not telegrame_exist:
            telegrame_noti = Notification('telegrame')
            db.session.add(telegrame_noti)
            db.session.commit()

    return app
