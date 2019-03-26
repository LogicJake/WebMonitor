from flask_login import current_user
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView


class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    column_labels = {
        'name': '用户名',
        'password': '密码',
    }

    can_create = False
    can_delete = False
