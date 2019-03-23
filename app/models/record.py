from .. import db
from datetime import datetime


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    url = db.Column(db.String(64), nullable=False)
    selector_type = db.Column(db.String(64), nullable=False)
    selector = db.Column(db.String(64), nullable=False)
    is_chrome = db.Column(db.String(64), nullable=False, default='no')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now)
