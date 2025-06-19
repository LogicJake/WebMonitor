from datetime import datetime
from api import db
from api.models.selector import Selector

# 任务和通知方式的关联表
task_notifications = db.Table('task_notifications',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('notification_id', db.Integer, db.ForeignKey('notifications.id'), primary_key=True)
)

class Task(db.Model):
    """任务模型"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='未命名任务')
    url = db.Column(db.String(500), nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    message = db.Column(db.Text)
    custom_headers = db.Column(db.Text)  # 存储自定义请求头的JSON字符串
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_check = db.Column(db.DateTime)
    last_status = db.Column(db.Integer)
    last_response_time = db.Column(db.Float)
    error_count = db.Column(db.Integer, default=0)
    consecutive_errors = db.Column(db.Integer, default=0)
    last_error = db.Column(db.Text)
    last_content = db.Column(db.Text)  # 存储上次解析的内容JSON字符串
    selectors = db.relationship('Selector', backref='task', lazy=True, cascade='all, delete-orphan')
    change_conditions = db.relationship('ChangeCondition', backref='task', lazy=True, cascade='all, delete-orphan', order_by='ChangeCondition.order_index')
    notifications = db.relationship('Notification', secondary=task_notifications, lazy='subquery',
                                  backref=db.backref('tasks', lazy=True))

    def __init__(self, url, interval, name=None, active=True, message=None, custom_headers=None):
        self.url = url
        self.interval = interval
        self.name = name or '未命名任务'
        self.active = active
        self.message = message
        self.custom_headers = custom_headers

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """将模型转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'interval': self.interval,
            'active': self.active,
            'message': self.message,
            'custom_headers': self.custom_headers,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'last_status': self.last_status,
            'last_response_time': self.last_response_time,
            'error_count': self.error_count,
            'consecutive_errors': self.consecutive_errors,
            'last_error': self.last_error,
            'last_content': self.last_content,
            'selectors': [selector.to_dict() for selector in self.selectors],
            'change_conditions': [condition.to_dict() for condition in self.change_conditions],
            'notifications': [notification.to_dict() for notification in self.notifications]
        }

    def __repr__(self):
        return f'<Task {self.id}: {self.url}>' 