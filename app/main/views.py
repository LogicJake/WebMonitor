# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 20:04:12
# @Last Modified time: 2019-03-14 21:17:03
from flask import Blueprint
from app.main.notification.notification_handler import new_handler

bp = Blueprint('main', __name__)


@bp.route('/send')
def test():
    handler = new_handler('mail')
    handler.send('835410808@qq.com', 'fuck')
    return 'test'
