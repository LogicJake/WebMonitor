class BaseError(Exception):
    """基础异常类"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class TaskNotFoundError(BaseError):
    """任务不存在异常"""
    pass

class ValidationError(BaseError):
    """数据验证异常"""
    pass

class DatabaseError(BaseError):
    """数据库操作异常"""
    pass

class ServiceError(BaseError):
    """服务层异常"""
    pass

class NotificationNotFoundError(Exception):
    """通知方式未找到错误"""
    pass 