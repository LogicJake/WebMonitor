from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user


class TaskStatusView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    can_create = False
    can_delete = False

    column_labels = {
        'task_id': '任务id',
        'task_name': '任务名称',
        'last_run': '上次运行时间',
        'last_status': '上次运行结果',
        'task_status': '任务状态',
        'task_type': '监控任务类型'
    }

    form_choices = {'work_status': [('run', 'run'), ('stop', 'stop')]}

    form_widget_args = {
        'task_id': {
            'readonly': True
        },
        'task_name': {
            'readonly': True
        },
        'task_type': {
            'readonly': True
        }
    }

    form_choices = {
        'task_status': [('run', 'run'), ('stop', 'stop')],
    }

    form_excluded_columns = ('last_run', 'last_status')
