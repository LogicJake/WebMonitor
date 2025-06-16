"""
日志服务模块

收集、存储和管理监控服务的日志信息
"""

import logging
import json
from datetime import datetime, timedelta
from collections import deque
from threading import Lock
from typing import List, Dict, Optional

class LogRecord:
    """日志记录类"""
    
    def __init__(self, level: str, message: str, timestamp: datetime = None, 
                 task_id: int = None, task_name: str = None, extra: dict = None):
        self.level = level
        self.message = message
        self.timestamp = timestamp or datetime.utcnow()
        self.task_id = task_id
        self.task_name = task_name
        self.extra = extra or {}
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'level': self.level,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'task_id': self.task_id,
            'task_name': self.task_name,
            'extra': self.extra
        }

class MonitorLogService:
    """监控日志服务"""
    
    def __init__(self, max_logs: int = 1000):
        self.max_logs = max_logs
        self.logs = deque(maxlen=max_logs)
        self.lock = Lock()
        
    def add_log(self, level: str, message: str, task_id: int = None, 
                task_name: str = None, extra: dict = None):
        """添加日志记录"""
        with self.lock:
            log_record = LogRecord(level, message, task_id=task_id, 
                                 task_name=task_name, extra=extra)
            self.logs.append(log_record)
    
    def get_logs(self, limit: int = 100, level: str = None, 
                 task_id: int = None) -> List[Dict]:
        """获取日志记录"""
        with self.lock:
            filtered_logs = []
            for log in reversed(self.logs):  # 最新的在前
                # 级别过滤
                if level and log.level.lower() != level.lower():
                    continue
                    
                # 任务过滤
                if task_id and log.task_id != task_id:
                    continue
                    
                filtered_logs.append(log.to_dict())
                
                # 限制数量
                if len(filtered_logs) >= limit:
                    break
            
            return filtered_logs
    
    def clear_logs(self):
        """清空日志"""
        with self.lock:
            self.logs.clear()
    
    def get_log_stats(self) -> Dict:
        """获取日志统计信息"""
        with self.lock:
            stats = {
                'total': len(self.logs),
                'info': 0,
                'warning': 0,
                'error': 0,
                'debug': 0
            }
            
            for log in self.logs:
                level = log.level.lower()
                if level in stats:
                    stats[level] += 1
            
            return stats

class MonitorLogHandler(logging.Handler):
    """自定义日志处理器，将日志发送到MonitorLogService"""
    
    def __init__(self, log_service: MonitorLogService):
        super().__init__()
        self.log_service = log_service
    
    def emit(self, record):
        """处理日志记录"""
        try:
            # 提取任务信息
            task_id = getattr(record, 'task_id', None)
            task_name = getattr(record, 'task_name', None)
            
            # 构建额外信息
            extra = {
                'logger_name': record.name,
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            }
            
            # 添加到日志服务
            self.log_service.add_log(
                level=record.levelname,
                message=record.getMessage(),
                task_id=task_id,
                task_name=task_name,
                extra=extra
            )
        except Exception:
            # 避免日志处理器本身出错
            pass

# 全局日志服务实例
monitor_log_service = MonitorLogService()

# 配置日志处理器
def setup_monitor_logging():
    """设置监控日志"""
    # 获取监控相关的logger
    monitor_logger = logging.getLogger('api.services.monitor_service')
    
    # 添加自定义处理器
    handler = MonitorLogHandler(monitor_log_service)
    handler.setLevel(logging.INFO)
    
    # 设置格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # 添加到logger
    monitor_logger.addHandler(handler)
    monitor_logger.setLevel(logging.INFO)

# 便捷的日志记录函数
def log_monitor_info(message: str, task_id: int = None, task_name: str = None, **kwargs):
    """记录信息日志"""
    monitor_log_service.add_log('INFO', message, task_id, task_name, kwargs)

def log_monitor_warning(message: str, task_id: int = None, task_name: str = None, **kwargs):
    """记录警告日志"""
    monitor_log_service.add_log('WARNING', message, task_id, task_name, kwargs)

def log_monitor_error(message: str, task_id: int = None, task_name: str = None, **kwargs):
    """记录错误日志"""
    monitor_log_service.add_log('ERROR', message, task_id, task_name, kwargs)

def log_monitor_debug(message: str, task_id: int = None, task_name: str = None, **kwargs):
    """记录调试日志"""
    monitor_log_service.add_log('DEBUG', message, task_id, task_name, kwargs) 