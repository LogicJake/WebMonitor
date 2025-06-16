from datetime import datetime
from api import db
import json

class Notification(db.Model):
    """通知方式模型"""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # email, webhook, dingtalk, wechat
    config = db.Column(db.Text, nullable=False)  # JSON格式存储配置
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, type, config):
        self.name = name
        self.type = type
        self.config = json.dumps(config) if isinstance(config, dict) else config

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_config(self):
        """获取配置字典"""
        try:
            return json.loads(self.config) if self.config else {}
        except:
            return {}

    def set_config(self, config_dict):
        """设置配置字典"""
        self.config = json.dumps(config_dict)

    def to_dict(self):
        """将模型转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'config': self.get_config(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Notification {self.id}: {self.type}>' 