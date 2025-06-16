from flask import Blueprint, jsonify, request
from api.services.log_service import monitor_log_service

log_bp = Blueprint('log', __name__)

@log_bp.route('/logs', methods=['GET'])
def get_logs():
    """获取监控日志"""
    try:
        # 获取查询参数
        limit = request.args.get('limit', 100, type=int)
        level = request.args.get('level')
        task_id = request.args.get('task_id', type=int)
        
        # 限制参数范围
        limit = min(max(limit, 1), 500)  # 1-500
        
        # 获取日志
        logs = monitor_log_service.get_logs(
            limit=limit,
            level=level,
            task_id=task_id
        )
        
        return jsonify({
            'success': True,
            'data': logs,
            'total': len(logs)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@log_bp.route('/logs/stats', methods=['GET'])
def get_log_stats():
    """获取日志统计信息"""
    try:
        stats = monitor_log_service.get_log_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@log_bp.route('/logs/clear', methods=['POST'])
def clear_logs():
    """清空日志"""
    try:
        monitor_log_service.clear_logs()
        return jsonify({
            'success': True,
            'message': '日志已清空'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 