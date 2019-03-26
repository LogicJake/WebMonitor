from .. import db
from flask_login import logout_user
from sqlalchemy import event
from flask import redirect


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


def after_update_listener(mapper, connection, target):
    logout_user()
    redirect('/')


event.listen(User, 'after_update', after_update_listener)
