from datetime import datetime
from api.models.task import Task
from api.models.selector import Selector
from api.models.change_condition import ChangeCondition
from api import db
from api.models.notification import Notification
from api.utils.exceptions import TaskNotFoundError, ValidationError
from api.config.config import Config

class TaskService:
    """任务服务类"""
    
    @staticmethod
    def get_all_tasks():
        """获取所有任务"""
        return Task.query.all()
    
    @staticmethod
    def get_task_by_id(task_id):
        """根据ID获取任务"""
        return Task.query.get_or_404(task_id)
    
    @staticmethod
    def create_task(data):
        """创建新任务"""
        # 验证通知方式
        if 'notification_ids' not in data or not data['notification_ids']:
            raise ValidationError('至少需要选择一个通知方式')
        
        # 验证通知方式是否存在
        notification_ids = data['notification_ids']
        notifications = Notification.query.filter(Notification.id.in_(notification_ids)).all()
        if len(notifications) != len(notification_ids):
            raise ValidationError('选择的通知方式中包含无效的ID')

        task = Task(
            url=data['url'],
            interval=data['interval'],
            name=data.get('name'),
            active=data.get('active', True),
            message=data.get('message'),
            custom_headers=data.get('custom_headers'),
            use_playwright=data.get('use_playwright', False)
        )
        
        # 添加通知方式关联
        task.notifications = notifications
        
        # 创建选择器
        if 'selectors' in data:
            for selector_data in data['selectors']:
                selector = Selector(
                    task_id=task.id,
                    name=selector_data['name'],
                    type=selector_data['type'],
                    expression=selector_data['expression'],
                    regex_expression=selector_data.get('regex_expression')
                )
                task.selectors.append(selector)
        
        # 创建变化判断条件
        if 'change_conditions' in data:
            for index, condition_data in enumerate(data['change_conditions']):
                condition = ChangeCondition(
                    task_id=task.id,
                    element_name=condition_data['element_name'],
                    operator=condition_data['operator'],
                    compare_value=condition_data.get('compare_value'),
                    order_index=index
                )
                task.change_conditions.append(condition)
        
        return task.save()
    
    @staticmethod
    def update_task(task_id, data):
        """更新任务"""
        task = Task.query.get_or_404(task_id)
        
        # 更新任务基本信息
        if 'name' in data:
            task.name = data['name']
        if 'url' in data:
            task.url = data['url']
        if 'interval' in data:
            task.interval = data['interval']
        if 'active' in data:
            task.active = data['active']
        if 'message' in data:
            task.message = data['message']
        if 'custom_headers' in data:
            task.custom_headers = data['custom_headers']
        if 'use_playwright' in data:
            task.use_playwright = data['use_playwright']
        
        # 更新通知方式
        if 'notification_ids' in data:
            if not data['notification_ids']:
                raise ValidationError('至少需要选择一个通知方式')
            
            notification_ids = data['notification_ids']
            notifications = Notification.query.filter(Notification.id.in_(notification_ids)).all()
            if len(notifications) != len(notification_ids):
                raise ValidationError('选择的通知方式中包含无效的ID')
            
            task.notifications = notifications
        
        # 更新选择器
        if 'selectors' in data:
            # 删除现有的选择器
            task.selectors = []
            
            # 添加新的选择器
            for selector_data in data['selectors']:
                selector = Selector(
                    task_id=task.id,
                    name=selector_data['name'],
                    type=selector_data['type'],
                    expression=selector_data['expression'],
                    regex_expression=selector_data.get('regex_expression')
                )
                task.selectors.append(selector)
        
        # 更新变化判断条件
        if 'change_conditions' in data:
            # 删除现有的变化条件
            task.change_conditions = []
            
            # 添加新的变化条件
            for index, condition_data in enumerate(data['change_conditions']):
                condition = ChangeCondition(
                    task_id=task.id,
                    element_name=condition_data['element_name'],
                    operator=condition_data['operator'],
                    compare_value=condition_data.get('compare_value'),
                    order_index=index
                )
                task.change_conditions.append(condition)
        
        task.updated_at = datetime.utcnow()
        return task.save()
    
    @staticmethod
    def delete_task(task_id):
        """删除任务"""
        task = Task.query.get_or_404(task_id)
        task.delete()
        return True

    @staticmethod
    def update_task_status(task_id, status, response_time=None, error=None):
        """更新任务状态"""
        task = Task.query.get_or_404(task_id)
        
        task.last_check = datetime.utcnow()
        task.last_status = status
        task.last_response_time = response_time
        
        if error:
            task.error_count += 1
            task.consecutive_errors += 1
            task.last_error = str(error)
        else:
            task.consecutive_errors = 0
            task.last_error = None
        
        return task.save()
