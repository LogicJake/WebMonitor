from flask import Blueprint, jsonify
from api.services.monitor_service import monitor_service

monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/monitor/status', methods=['GET'])
def get_monitor_status():
    """获取监控服务状态"""
    try:
        status = monitor_service.get_status()
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@monitor_bp.route('/monitor/start', methods=['POST'])
def start_monitor():
    """启动监控服务"""
    try:
        if monitor_service.start():
            return jsonify({
                'success': True,
                'message': '监控服务已启动'
            })
        else:
            return jsonify({
                'success': True,
                'message': '监控服务已在运行中'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@monitor_bp.route('/monitor/stop', methods=['POST'])
def stop_monitor():
    """停止监控服务"""
    try:
        if monitor_service.stop():
            return jsonify({
                'success': True,
                'message': '监控服务已停止'
            })
        else:
            return jsonify({
                'success': True,
                'message': '监控服务已停止'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 