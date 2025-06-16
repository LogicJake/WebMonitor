import os
import sys
import signal
import atexit
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from api.config.config import get_config
from api.controllers.task_controller import task_bp
from api.controllers.notification_controller import notification_bp
from api.controllers.monitor_controller import monitor_bp
from api.controllers.log_controller import log_bp
from api.services.monitor_service import monitor_service
from api.services.log_service import setup_monitor_logging
from api import db

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(get_config())
    
    # 初始化扩展
    db.init_app(app)
    CORS(app)
    
    # 将应用实例传递给监控服务
    monitor_service.app = app
    
    # 添加CORS响应头
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:8080', 'http://127.0.0.1:8080']:
            response.headers.add('Access-Control-Allow-Origin', origin)
        else:
            response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    # 注册蓝图
    app.register_blueprint(task_bp, url_prefix='/api')
    app.register_blueprint(notification_bp, url_prefix='/api')
    app.register_blueprint(monitor_bp, url_prefix='/api')
    app.register_blueprint(log_bp, url_prefix='/api')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    # 初始化监控日志
    setup_monitor_logging()
    
    return app

def start_monitor_service():
    """启动监控服务"""
    try:
        logger.info("正在启动监控服务...")
        if monitor_service.start():
            logger.info("监控服务启动成功")
        else:
            logger.warning("监控服务已在运行中")
    except Exception as e:
        logger.error(f"启动监控服务失败: {e}")

def stop_monitor_service():
    """停止监控服务"""
    try:
        logger.info("正在停止监控服务...")
        if monitor_service.stop():
            logger.info("监控服务停止成功")
        else:
            logger.info("监控服务已停止")
    except Exception as e:
        logger.error(f"停止监控服务失败: {e}")

def signal_handler(signum, frame):
    """信号处理器"""
    logger.info(f"接收到信号 {signum}，正在关闭应用...")
    stop_monitor_service()
    sys.exit(0)

if __name__ == '__main__':
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 注册退出处理器
    atexit.register(stop_monitor_service)
    
    try:
        # 创建应用
        app = create_app()
        
        # 在应用上下文中启动监控服务
        with app.app_context():
            start_monitor_service()
            
            logger.info("=" * 50)
            logger.info("Flask应用和监控服务已启动")
            logger.info("Web服务: http://127.0.0.1:5000")
            logger.info("监控服务: 后台运行")
            logger.info("=" * 50)
            
            # 启动Flask应用
            app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
            
    except KeyboardInterrupt:
        logger.info("接收到键盘中断")
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        stop_monitor_service()
        sys.exit(1)