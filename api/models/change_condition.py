from api import db

class ChangeCondition(db.Model):
    """变化判断条件模型"""
    __tablename__ = 'change_conditions'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    element_name = db.Column(db.String(100), nullable=False)  # 要判断的元素名称
    operator = db.Column(db.String(20), nullable=False)  # 操作符：contains, not_contains, greater_than, less_than, increased, decreased
    compare_value = db.Column(db.String(500), nullable=True)  # 比较值（对于increased/decreased可为空）
    order_index = db.Column(db.Integer, nullable=False, default=0)  # 判断顺序
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, task_id, element_name, operator, compare_value=None, order_index=0):
        self.task_id = task_id
        self.element_name = element_name
        self.operator = operator
        self.compare_value = compare_value
        self.order_index = order_index

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'element_name': self.element_name,
            'operator': self.operator,
            'compare_value': self.compare_value,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 