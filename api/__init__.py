from flask_sqlalchemy import SQLAlchemy

# 初始化数据库
db = SQLAlchemy()

# 导入所有模型以确保它们被注册
from api.models.task import Task
from api.models.selector import Selector
from api.models.change_condition import ChangeCondition
from api.models.notification import Notification