# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 19:33:23
# @Last Modified time: 2019-03-13 17:06:37
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from app.model_views import RecordView

db = SQLAlchemy()
admin = Admin(name='I AM WATCHING YOU', template_mode='bootstrap3')


def create_app(config_name):
    app = Flask(__name__)
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

    from app.models.record import Record
    admin.add_view(RecordView(Record, db.session, name='监控管理'))

    with app.test_request_context():
        db.create_all()

    return app
