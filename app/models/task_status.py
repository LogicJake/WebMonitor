from .. import db
from datetime import datetime
from sqlalchemy import event


class TaskStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)
    task_name = db.Column(db.String(32), nullable=False)
    last_run = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_status = db.Column(db.String(64), nullable=False, default='创建任务成功')
    task_status = db.Column(db.String(32), nullable=False, default='run')

    def __init__(self, task_id, task_name):
        self.task_id = task_id
        self.task_name = task_name


def after_update_listener(mapper, connection, target):
    from app.main.scheduler import add_job, remove_job

    if target.task_status == 'run':
        from app.models.task import Task
        task = Task.__table__

        select_res = connection.execute(
            task.select().where(Task.id == target.id))

        for t in select_res:
            add_job(target.id, t[6])
    else:
        remove_job(target.id)


event.listen(TaskStatus, 'after_update', after_update_listener)
