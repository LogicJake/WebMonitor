from datetime import datetime
from api.models.notification import Notification
from api import db
from api.utils.exceptions import NotificationNotFoundError, ValidationError

class NotificationService:
    """通知方式服务类"""
    
    @staticmethod
    def get_all_notifications():
        """获取所有通知方式"""
        return Notification.query.all()
    
    @staticmethod
    def get_notification_by_id(notification_id):
        """根据ID获取通知方式"""
        return Notification.query.get_or_404(notification_id)
    
    @staticmethod
    def create_notification(data):
        """创建新通知方式"""
        # 验证必填字段
        if not data.get('name'):
            raise ValidationError('通知方式名称不能为空')
        if not data.get('type'):
            raise ValidationError('通知类型不能为空')
        if not data.get('config'):
            raise ValidationError('通知配置不能为空')

        # 验证通知类型
        valid_types = ['email', 'webhook', 'dingtalk', 'wechat']
        if data['type'] not in valid_types:
            raise ValidationError(f'通知类型必须是以下之一: {", ".join(valid_types)}')

        # 根据类型验证配置
        NotificationService._validate_config(data['type'], data['config'])

        notification = Notification(
            name=data['name'],
            type=data['type'],
            config=data['config']
        )
        
        return notification.save()
    
    @staticmethod
    def update_notification(notification_id, data):
        """更新通知方式"""
        notification = Notification.query.get_or_404(notification_id)
        
        if 'name' in data:
            notification.name = data['name']
        if 'type' in data:
            if data['type'] not in ['email', 'webhook', 'dingtalk', 'wechat']:
                raise ValidationError('无效的通知类型')
            notification.type = data['type']
        if 'config' in data:
            NotificationService._validate_config(data.get('type', notification.type), data['config'])
            notification.set_config(data['config'])
        
        return notification.save()
    
    @staticmethod
    def delete_notification(notification_id):
        """删除通知方式"""
        notification = Notification.query.get_or_404(notification_id)
        notification.delete()
        return True
    
    @staticmethod
    def _validate_config(notification_type, config):
        """验证通知配置"""
        if notification_type == 'email':
            if not config.get('email'):
                raise ValidationError('邮箱地址不能为空')
            if not config.get('smtp_server'):
                raise ValidationError('SMTP服务器不能为空')
            if not config.get('smtp_port'):
                raise ValidationError('SMTP端口不能为空')
        elif notification_type == 'webhook':
            if not config.get('url'):
                raise ValidationError('Webhook URL不能为空')
        elif notification_type == 'dingtalk':
            if not config.get('webhook_url'):
                raise ValidationError('钉钉机器人Webhook URL不能为空')
        elif notification_type == 'wechat':
            if not config.get('webhook_url'):
                raise ValidationError('企业微信机器人Webhook URL不能为空') 