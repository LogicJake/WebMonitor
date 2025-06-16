from flask import Blueprint, request, jsonify
from api.services.task_service import TaskService
from api.utils.exceptions import TaskNotFoundError, ValidationError
from api.models.task import Task

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """获取所有任务"""
    try:
        tasks = TaskService.get_all_tasks()
        return jsonify({
            'success': True,
            'data': [task.to_dict() for task in tasks]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_bp.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """获取单个任务"""
    try:
        task = TaskService.get_task_by_id(task_id)
        return jsonify({
            'success': True,
            'data': task.to_dict()
        })
    except TaskNotFoundError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_bp.route('/task', methods=['POST'])
def create_task():
    """创建新任务"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '无效的请求数据'
            }), 400
        
        task = TaskService.create_task(data)
        
        return jsonify({
            'success': True,
            'data': task.to_dict()
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

@task_bp.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """更新任务"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '无效的请求数据'
            }), 400
        
        task = TaskService.update_task(task_id, data)
        return jsonify({
            'success': True,
            'data': task.to_dict()
        })
    except TaskNotFoundError as e:
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

@task_bp.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """删除任务"""
    try:
        TaskService.delete_task(task_id)
        return jsonify({
            'success': True,
            'message': '任务已删除'
        })
    except TaskNotFoundError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
