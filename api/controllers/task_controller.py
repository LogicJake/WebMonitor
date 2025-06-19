from flask import Blueprint, request, jsonify
from api.services.task_service import TaskService
from api.services.monitor_service import MonitorService
from api.utils.exceptions import TaskNotFoundError, ValidationError
from api.services.log_service import log_monitor_info, log_monitor_error
import traceback

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_all_tasks():
    """获取所有任务"""
    try:
        tasks = TaskService.get_all_tasks()
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """获取单个任务"""
    try:
        task = TaskService.get_task_by_id(task_id)
        return jsonify(task.to_dict())
    except TaskNotFoundError:
        return jsonify({'error': '任务不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """创建任务"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        task = TaskService.create_task(data)
        return jsonify(task.to_dict()), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """更新任务"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        task = TaskService.update_task(task_id, data)
        return jsonify(task.to_dict())
    except TaskNotFoundError:
        return jsonify({'error': '任务不存在'}), 404
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """删除任务"""
    try:
        TaskService.delete_task(task_id)
        return jsonify({'message': '任务删除成功'})
    except TaskNotFoundError:
        return jsonify({'error': '任务不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@task_bp.route('/tasks/test', methods=['POST'])
def test_task_config():
    """测试任务配置
    
    统一的任务测试接口，支持编辑和新增模式。
    不需要保存任务到数据库，直接使用传入的配置进行测试。
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        send_notification = data.get('send_notification', False)
        
        # 验证必要字段
        required_fields = ['url', 'interval', 'selectors']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必要字段: {field}'}), 400
        
        # 验证检查间隔
        interval = data.get('interval')
        if not isinstance(interval, (int, float)) or interval < 60:
            return jsonify({'error': '检查间隔必须至少为60秒（1分钟）'}), 400
        
        # 创建临时任务对象（不保存到数据库）
        from api.models.task import Task
        from api.models.selector import Selector
        from api.models.change_condition import ChangeCondition
        
        # 创建临时任务对象
        temp_task = Task(
            url=data['url'],
            interval=data['interval'],
            name=data.get('name', '测试任务'),
            active=data.get('active', True),
            message=data.get('message'),
            custom_headers=data.get('custom_headers'),
            use_playwright=data.get('use_playwright', False)
        )
        temp_task.id = 0  # 临时ID
        
        # 创建临时选择器
        temp_task.selectors = []
        for selector_data in data.get('selectors', []):
            selector = Selector(
                task_id=0,
                name=selector_data['name'],
                type=selector_data['type'],
                expression=selector_data['expression'],
                regex_expression=selector_data.get('regex_expression')
            )
            temp_task.selectors.append(selector)
        
        # 创建临时变化判断条件
        temp_task.change_conditions = []
        for condition_data in data.get('change_conditions', []):
            condition = ChangeCondition(
                task_id=0,
                element_name=condition_data['element_name'],
                operator=condition_data['operator'],
                compare_value=condition_data.get('compare_value'),
                order_index=len(temp_task.change_conditions)
            )
            temp_task.change_conditions.append(condition)
        
        # 创建临时通知方式关联
        temp_task.notifications = []
        if data.get('notification_ids'):
            from api.models.notification import Notification
            notifications = Notification.query.filter(Notification.id.in_(data['notification_ids'])).all()
            temp_task.notifications = notifications
        
        # 创建监控服务实例进行测试
        from flask import current_app
        monitor_service = MonitorService(current_app._get_current_object())
        
        log_monitor_info(f"开始测试任务配置: {temp_task.url}", task_name=temp_task.name)
        
        # 执行测试
        result = monitor_service.test_task(temp_task, send_notification)
        
        return jsonify(result)
        
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log_monitor_error(f"测试任务配置失败: {str(e)}")
        return jsonify({
            'error': f'测试失败: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500
