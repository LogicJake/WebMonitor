from api import db

class Selector(db.Model):
    __tablename__ = 'selectors'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # xpath, css, jsonpath
    expression = db.Column(db.String(500), nullable=False)
    regex_expression = db.Column(db.String(500), nullable=True)  # 正则表达式，用于二次提取
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, task_id, name, type, expression, regex_expression=None):
        self.task_id = task_id
        self.name = name
        self.type = type
        self.expression = expression
        self.regex_expression = regex_expression

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'name': self.name,
            'type': self.type,
            'expression': self.expression,
            'regex_expression': self.regex_expression,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 