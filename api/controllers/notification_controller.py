from flask import Blueprint, request, jsonify
from api.services.notification_service import NotificationService
from api.utils.exceptions import NotificationNotFoundError, ValidationError

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/notifications', methods=['GET'])
def get_notifications():
    """获取所有通知方式"""
    try:
        notifications = NotificationService.get_all_notifications()
        return jsonify({
            'success': True,
            'data': [notification.to_dict() for notification in notifications]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@notification_bp.route('/notification/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    """获取单个通知方式"""
    try:
        notification = NotificationService.get_notification_by_id(notification_id)
        return jsonify({
            'success': True,
            'data': notification.to_dict()
        })
    except NotificationNotFoundError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@notification_bp.route('/notification', methods=['POST'])
def create_notification():
    """创建新通知方式"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '无效的请求数据'
            }), 400
        
        notification = NotificationService.create_notification(data)
        
        return jsonify({
            'success': True,
            'data': notification.to_dict()
        }), 201
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@notification_bp.route('/notification/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
    """更新通知方式"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '无效的请求数据'
            }), 400
        
        notification = NotificationService.update_notification(notification_id, **data)
        return jsonify({
            'success': True,
            'data': notification.to_dict()
        })
    except NotificationNotFoundError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@notification_bp.route('/notification/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """删除通知方式"""
    try:
        NotificationService.delete_notification(notification_id)
        return jsonify({
            'success': True,
            'message': '通知方式已删除'
        })
    except NotificationNotFoundError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@notification_bp.route('/notification/<int:notification_id>/toggle', methods=['POST'])
def toggle_notification(notification_id):
    """切换通知方式状态"""
    try:
        notification = NotificationService.toggle_notification(notification_id)
        return jsonify({
            'success': True,
            'data': notification.to_dict()
        })
    except NotificationNotFoundError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 