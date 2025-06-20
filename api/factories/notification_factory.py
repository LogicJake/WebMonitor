"""
通知发送器工厂模块

提供各种类型的通知发送器，支持动态注册新的通知类型。
"""

import requests
import json
from abc import ABC, abstractmethod
from datetime import datetime


class NotificationSender(ABC):
    """通知发送器基类"""
    
    @abstractmethod
    def send(self, notification, task, message):
        """发送通知
        
        Args:
            notification: 通知配置对象
            task: 任务对象
            message: 通知消息内容
            
        Returns:
            dict: 发送结果
                {
                    'success': bool,
                    'message': str,
                    'error': str
                }
        """
        pass


class WebhookSender(NotificationSender):
    """Webhook通知发送器"""
    
    def send(self, notification, task, message):
        try:
            config = notification.get_config()
            url = config.get('url')
            
            if not url:
                return {
                    'success': False,
                    'message': None,
                    'error': 'Webhook URL未配置'
                }
                
            payload = {
                'task_name': task.name,
                'task_url': task.url,
                'message': message,
                'timestamp': datetime.utcnow().isoformat(),
                'task_id': task.id
            }
            
            # 支持自定义请求头
            headers = {'Content-Type': 'application/json'}
            if 'headers' in config:
                headers.update(config['headers'])
            
            response = requests.post(
                url, 
                json=payload, 
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': f'Webhook通知发送成功: {response.status_code}',
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'message': None,
                    'error': f'Webhook响应错误: {response.status_code}'
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'message': None,
                'error': 'Webhook请求超时'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'message': None,
                'error': 'Webhook连接失败'
            }
        except Exception as e:
            return {
                'success': False,
                'message': None,
                'error': f'Webhook发送失败: {str(e)}'
            }


class DingTalkSender(NotificationSender):
    """钉钉通知发送器"""
    
    def send(self, notification, task, message):
        try:
            config = notification.get_config()
            webhook_url = config.get('webhook_url')
            
            if not webhook_url:
                return {
                    'success': False,
                    'message': None,
                    'error': '钉钉Webhook URL未配置'
                }
            
            # 构建钉钉消息格式
            payload = {
                'msgtype': 'text',
                'text': {
                    'content': message
                }
            }
            
            # 支持@所有人或@特定用户
            if config.get('at_all'):
                payload['at'] = {'isAtAll': True}
            elif config.get('at_mobiles'):
                payload['at'] = {
                    'atMobiles': config['at_mobiles'],
                    'isAtAll': False
                }
            
            response = requests.post(
                webhook_url, 
                json=payload, 
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('errcode') == 0:
                    return {
                        'success': True,
                        'message': '钉钉通知发送成功',
                        'error': None
                    }
                else:
                    return {
                        'success': False,
                        'message': None,
                        'error': f'钉钉API错误: {result.get("errmsg", "未知错误")}'
                    }
            else:
                return {
                    'success': False,
                    'message': None,
                    'error': f'钉钉响应错误: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': None,
                'error': f'钉钉通知发送失败: {str(e)}'
            }


class WeChatSender(NotificationSender):
    """企业微信通知发送器"""
    
    def send(self, notification, task, message):
        try:
            config = notification.get_config()
            webhook_url = config.get('webhook_url')
            
            if not webhook_url:
                return {
                    'success': False,
                    'message': None,
                    'error': '企业微信Webhook URL未配置'
                }
            
            # 构建企业微信消息格式
            payload = {
                'msgtype': 'text',
                'text': {
                    'content': message
                }
            }
            
            # 支持@特定用户
            if config.get('mentioned_list'):
                payload['text']['mentioned_list'] = config['mentioned_list']
            elif config.get('mentioned_mobile_list'):
                payload['text']['mentioned_mobile_list'] = config['mentioned_mobile_list']
            
            response = requests.post(
                webhook_url, 
                json=payload, 
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('errcode') == 0:
                    return {
                        'success': True,
                        'message': '企业微信通知发送成功',
                        'error': None
                    }
                else:
                    return {
                        'success': False,
                        'message': None,
                        'error': f'企业微信API错误: {result.get("errmsg", "未知错误")}'
                    }
            else:
                return {
                    'success': False,
                    'message': None,
                    'error': f'企业微信响应错误: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': None,
                'error': f'企业微信通知发送失败: {str(e)}'
            }


class EmailSender(NotificationSender):
    """邮件通知发送器"""
    
    def send(self, notification, task, message):
        try:
            config = notification.get_config()
            
            # 检查必要配置
            required_fields = ['smtp_server', 'smtp_port', 'username', 'password', 'email']
            for field in required_fields:
                if not config.get(field):
                    return {
                        'success': False,
                        'message': None,
                        'error': f'邮件配置缺少必要字段: {field}'
                    }
            
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = config['username']
            msg['To'] = config['email']
            msg['Subject'] = f"网页监控通知 - {task.name}"
            
            # 邮件正文
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            # 发送邮件
            server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
            
            server.login(config['username'], config['password'])
            server.send_message(msg)
            server.quit()
            
            return {
                'success': True,
                'message': '邮件通知发送成功',
                'error': None
            }
            
        except ImportError:
            return {
                'success': False,
                'message': None,
                'error': '邮件功能需要Python标准库支持'
            }
        except Exception as e:
            return {
                'success': False,
                'message': None,
                'error': f'邮件发送失败: {str(e)}'
            }


class NotificationSenderFactory:
    """通知发送器工厂"""
    
    _senders = {
        'webhook': WebhookSender(),
        'dingtalk': DingTalkSender(),
        'wechat': WeChatSender(),
        'email': EmailSender(),
    }
    
    @classmethod
    def get_sender(cls, notification_type):
        """获取通知发送器
        
        Args:
            notification_type: 通知类型
            
        Returns:
            NotificationSender: 对应的发送器实例
            
        Raises:
            ValueError: 不支持的通知类型
        """
        sender = cls._senders.get(notification_type.lower())
        if not sender:
            raise ValueError(f"不支持的通知类型: {notification_type}")
        return sender
    
    @classmethod
    def register_sender(cls, notification_type, sender):
        """注册新的通知发送器
        
        Args:
            notification_type: 通知类型名称
            sender: 发送器实例
            
        Raises:
            TypeError: 发送器类型错误
        """
        if not isinstance(sender, NotificationSender):
            raise TypeError("发送器必须继承自NotificationSender")
        cls._senders[notification_type.lower()] = sender
    
    @classmethod
    def unregister_sender(cls, notification_type):
        """注销通知发送器
        
        Args:
            notification_type: 通知类型名称
            
        Returns:
            bool: 是否成功注销
        """
        return cls._senders.pop(notification_type.lower(), None) is not None
    
    @classmethod
    def get_supported_types(cls):
        """获取支持的通知类型列表
        
        Returns:
            list: 支持的通知类型列表
        """
        return list(cls._senders.keys())
    
    @classmethod
    def is_supported(cls, notification_type):
        """检查是否支持指定的通知类型
        
        Args:
            notification_type: 通知类型
            
        Returns:
            bool: 是否支持
        """
        return notification_type.lower() in cls._senders
    
    @classmethod
    def send_notification(cls, notification, task, message):
        """发送通知的便捷方法
        
        Args:
            notification: 通知配置对象
            task: 任务对象
            message: 通知消息
            
        Returns:
            dict: 发送结果
        """
        try:
            sender = cls.get_sender(notification.type)
            return sender.send(notification, task, message)
        except ValueError as e:
            return {
                'success': False,
                'message': None,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'message': None,
                'error': f'发送通知时发生未知错误: {str(e)}'
            }


# 使用示例和扩展指南
"""
如何添加新的通知类型：

1. 创建发送器类：
class CustomSender(NotificationSender):
    def send(self, notification, task, message):
        try:
            config = notification.get_config()
            # 实现自定义发送逻辑
            # ...
            return {
                'success': True,
                'message': '发送成功',
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'message': None,
                'error': f'发送失败: {str(e)}'
            }

2. 注册发送器：
NotificationSenderFactory.register_sender('custom', CustomSender())

3. 使用：
result = NotificationSenderFactory.send_notification(notification, task, message)

支持的通知类型：
- webhook: HTTP Webhook通知
- dingtalk: 钉钉机器人通知
- wechat: 企业微信机器人通知
- email: 邮件通知
""" 