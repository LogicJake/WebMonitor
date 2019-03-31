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
    task_type = db.Column(db.String(32), nullable=False, default='html')

    def __init__(self, task_id, task_name, task_status='html'):
        self.task_id = task_id
        self.task_name = task_name
        self.task_status = task_status


def after_update_listener(mapper, connection, target):
    from app.main.scheduler import add_job, remove_job

    if target.task_status == 'run':
        if target.task_type == 'html':
            from app.models.task import Task
            task = Task.__table__
            select_res = connection.execute(
                task.select().where(Task.id == target.task_id))

            for t in select_res:
                remove_job(target.task_id)
                add_job(target.task_id, t[6])
        elif target.task_type == 'rss':
            from app.models.rss_task import RSSTask
            rss_task = RSSTask.__table__
            select_res = connection.execute(
                rss_task.select().where(RSSTask.id == target.task_id))

            for t in select_res:
                remove_job(target.task_id, 'rss')
                add_job(target.task_id, t[3], 'rss')
    else:
        remove_job(target.id)


event.listen(TaskStatus, 'after_update', after_update_listener)
