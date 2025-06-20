import time
import requests
import hashlib
import json
import threading
import re
from datetime import datetime, timedelta
from api.models.task import Task
from api.models.notification import Notification
from api import db
from flask import current_app
from api.factories.selector_factory import SelectorParserFactory
from api.factories.notification_factory import NotificationSenderFactory
from api.factories.fetcher_factory import FetcherFactory
from api.services.log_service import log_monitor_info, log_monitor_warning, log_monitor_error, log_monitor_debug
from typing import List, Dict

class MonitorService:
    def __init__(self, app=None):
        self.app = app
        self.running = False
        self.monitor_thread = None
        self.last_check_time = None
        self.check_count = 0
        self.error_count = 0
        
    def regex_extract(self, text, regex_expression):
        """使用正则表达式从文本中提取内容
        
        Args:
            text: 待提取的文本
            regex_expression: 正则表达式
            
        Returns:
            str or None: 提取结果
        """
        if not regex_expression or not text:
            return text
            
        try:
            match = re.search(regex_expression, text)
            if match:
                # 如果有分组，返回第一个分组，否则返回整个匹配
                return match.group(1) if match.groups() else match.group(0)
            return None
        except Exception as e:
            raise ValueError(f"正则表达式解析错误: {e}")
        
    def start(self):
        """启动监控服务"""
        if self.running:
            log_monitor_warning("监控服务已在运行中")
            return False
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        log_monitor_info("网页监控服务已启动")
        return True
        
    def stop(self):
        """停止监控服务"""
        if not self.running:
            return False
            
        self.running = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        log_monitor_info("网页监控服务已停止")
        return True
        
    def get_status(self):
        """获取监控服务状态"""
        # 获取活跃任务数量
        monitored_tasks = 0
        try:
            if self.app:
                with self.app.app_context():
                    monitored_tasks = Task.query.filter_by(active=True).count()
        except:
            pass
            
        return {
            'running': self.running,
            'thread_alive': self.monitor_thread.is_alive() if self.monitor_thread else False,
            'monitored_tasks': monitored_tasks,
            'last_check_time': self.last_check_time.isoformat() if self.last_check_time else None,
            'check_count': self.check_count,
            'error_count': self.error_count
        }
        
    def _monitor_loop(self):
        """主监控循环"""
        log_monitor_info("监控循环已启动")
        
        while self.running:
            try:
                self.last_check_time = datetime.utcnow()
                self._check_all_tasks()
                self.check_count += 1
                
                # 每10秒检查一次
                for _ in range(100):  # 10秒 = 100 * 0.1秒
                    if not self.running:
                        break
                    time.sleep(0.1)
                    
            except Exception as e:
                self.error_count += 1
                log_monitor_error(f"监控循环出错: {e}")
                time.sleep(30)  # 出错时等待更长时间
                
        log_monitor_info("监控循环已退出")
    
    def test_task(self, task, send_notification=False):
        """测试单个任务执行
        
        Args:
            task: 任务对象
            send_notification: 是否发送通知
            
        Returns:
            dict: 测试结果
        """
        try:
            log_monitor_info(f"开始测试任务: {task.url}", task_id=task.id, task_name=task.name)
            
            # 请求网页
            fetch_result = self._fetch_webpage(task)
            
            if not fetch_result['success']:
                return {
                    'success': False,
                    'error': fetch_result['error'],
                    'response_time': fetch_result['response_time']
                }
                
            # 解析内容
            parse_results = self._parse_content(task, fetch_result['content'])
            
            if parse_results.get('error'):
                return {
                    'success': False,
                    'error': parse_results['error'],
                    'response_time': fetch_result['response_time']
                }
            
            # 进行模板替换
            formatted_message = self._replace_template_placeholders(task, parse_results['elements'])
            parse_results['formatted_message'] = formatted_message
            
            # 检查变化（不更新数据库）
            has_changed = self._check_content_change(task, parse_results, debug=True)
            
            result = {
                'success': True,
                'response_time': fetch_result['response_time'],
                'elements': parse_results['elements'],
                'formatted_message': formatted_message,
                'has_changed': has_changed,
                'notification_sent': False,
                'screenshot': fetch_result.get('screenshot')  # 包含截图信息
            }
            
            # 如果需要发送通知且有变化
            if send_notification and has_changed:
                try:
                    self._send_notifications(task, {
                        'elements': parse_results['elements'],
                        'formatted_message': formatted_message
                    })
                    result['notification_sent'] = True
                    log_monitor_info(f"测试任务通知已发送", task_id=task.id, task_name=task.name)
                except Exception as e:
                    result['notification_error'] = str(e)
                    log_monitor_error(f"测试任务发送通知失败: {e}", task_id=task.id, task_name=task.name)
            
            log_monitor_info(f"测试任务完成", task_id=task.id, task_name=task.name)
            return result
            
        except Exception as e:
            log_monitor_error(f"测试任务时出错: {e}", task_id=task.id, task_name=task.name)
            return {
                'success': False,
                'error': str(e)
            }
    
        
    def _check_all_tasks(self):
        """检查所有任务"""
        try:
            # 在应用上下文中执行数据库查询
            with self.app.app_context():
                # 获取所有活跃的任务
                tasks = Task.query.filter_by(active=True).all()
                
                for task in tasks:
                    if self._should_check_task(task):
                        # 在新线程中执行检查
                        thread = threading.Thread(
                            target=self._check_task,
                            args=(task.id,),
                            daemon=True
                        )
                        thread.start()
                    
        except Exception as e:
            log_monitor_error(f"检查任务列表时出错: {e}")
            
    def _should_check_task(self, task):
        """判断是否需要检查任务"""
        if not task.active:
            return False
            
        # 如果从未检查过，立即检查
        if not task.last_check:
            return True
            
        # 计算下次检查时间
        next_check = task.last_check + timedelta(seconds=task.interval)
        return datetime.utcnow() >= next_check
        
    def _fetch_webpage(self, task):
        """请求监控对象网页
        
        Args:
            task: 任务对象
            
        Returns:
            dict: 包含响应内容和响应时间的字典
                {
                    'success': bool,
                    'content': str,
                    'response_time': float,
                    'error': str
                }
        """
        # 使用工厂类统一处理网页抓取
        use_playwright = getattr(task, 'use_playwright', False)
        custom_headers = getattr(task, 'custom_headers', None)
        
        return FetcherFactory.fetch_webpage(
            url=task.url,
            use_playwright=use_playwright,
            custom_headers=custom_headers,
            timeout=30
        )
    


    def _check_task(self, task_id):
        """检查单个任务"""
        try:
            # 在应用上下文中重新获取任务对象以避免跨线程问题
            with self.app.app_context():
                task = Task.query.get(task_id)
                if not task:
                    return
                
                # 请求网页
                fetch_result = self._fetch_webpage(task)
                
                if not fetch_result['success']:
                    self._handle_error(task, fetch_result['error'], fetch_result['response_time'])
                    return
                    
                # 解析内容
                results = self._parse_content(task, fetch_result['content'])
                
                if results.get('error'):
                    self._handle_error(task, results['error'], fetch_result['response_time'])
                    return
                
                # 立即进行模板替换
                formatted_message = self._replace_template_placeholders(task, results['elements'])
                results['formatted_message'] = formatted_message
                    
                # 检查变化
                has_changed = self._check_content_change(task, results)
                
                # 更新任务状态
                self._update_task_status(task, True, fetch_result['response_time'], None)
                
                if has_changed:
                    log_monitor_info(f"检测到内容变化", task_id=task.id, task_name=task.name)
                    self._send_notifications(task, results)
                else:
                    log_monitor_debug(f"内容无变化", task_id=task.id, task_name=task.name)
                
        except Exception as e:
            log_monitor_error(f"检查任务时出错: {e}")
            try:
                with self.app.app_context():
                    task = Task.query.get(task_id)
                    if task:
                        self._handle_error(task, str(e), 0)
            except:
                pass
                
    def _parse_content(self, task, content):
        """解析页面内容"""
        results = {'elements': {}, 'error': None}
        
        try:
            for selector in task.selectors:
                try:
                    # 使用工厂模式获取对应的解析器
                    parser = SelectorParserFactory.get_parser(selector.type)
                    
                    # 执行解析
                    parsed_result = parser.parse(content, selector.expression)
                    
                    # 如果存在regex_expression，对解析结果进行正则表达式提取
                    if selector.regex_expression and parsed_result:
                        parsed_result = self.regex_extract(parsed_result, selector.regex_expression)
                    
                    results['elements'][selector.name] = parsed_result
                    
                except ValueError as e:
                    # 选择器解析错误
                    results['error'] = f"解析选择器 {selector.name} 出错: {e}"
                    break
                except Exception as e:
                    # 其他未知错误
                    results['error'] = f"解析选择器 {selector.name} 时发生未知错误: {e}"
                    break
                    
        except Exception as e:
            results['error'] = f"内容解析出错: {e}"
            
        return results
        
    def _check_content_change(self, task, current_results, debug=False):
        """检查内容变化
        
        Args:
            task: 任务对象
            current_results: 当前解析结果
            debug: 调试模式，为True时不更新数据库
        """
        try:
            # 如果任务有变化判断条件，使用自定义逻辑
            if task.change_conditions:
                return self._check_change_with_conditions(task, current_results, debug)
            
            # 默认逻辑：比较格式化消息模板的变化
            current_message = current_results.get('formatted_message', '')
            if not current_message:
                current_message = ''
            
            # 获取上次的格式化消息
            last_content = self._get_last_content(task)
            last_message = ''
            if last_content and last_content.get('formatted_message'):
                last_message = last_content['formatted_message']
            
            # 检查消息是否有变化
            has_changed = False
            if not last_content:
                if debug:
                    log_monitor_info(f"测试任务首次检查，无基准数据")
                else:
                    log_monitor_info(f"任务 {task.name} 首次检查，建立基准")
                has_changed = False
            else:
                has_changed = current_message != last_message
                if has_changed:
                    if debug:
                        log_monitor_info(f"测试任务消息模板内容发生变化")
                    else:
                        log_monitor_info(f"任务 {task.name} 消息模板内容发生变化")
                        log_monitor_debug(f"旧消息: {last_message}")
                        log_monitor_debug(f"新消息: {current_message}")
                else:
                    if debug:
                        log_monitor_info(f"测试任务消息模板内容无变化")
            
            # 只在非调试模式下更新数据库中的内容
            if not debug:
                full_content = {
                    'elements': current_results['elements'],
                    'formatted_message': current_message
                }
                task.last_content = json.dumps(full_content, sort_keys=True, ensure_ascii=False)
            
            return has_changed
            
        except Exception as e:
            error_msg = f"测试检查变化时出错: {e}" if debug else f"检查变化时出错: {e}"
            log_monitor_error(error_msg)
            return False

    def _check_change_with_conditions(self, task, current_results, debug=False):
        """使用自定义条件检查变化
        
        Args:
            task: 任务对象
            current_results: 当前解析结果
            debug: 调试模式，为True时不更新数据库
        """
        try:
            # 获取上次内容
            last_content = self._get_last_content(task)
            last_elements = last_content.get('elements', {}) if last_content else {}
            current_elements = current_results['elements']
            
            # 按顺序检查每个条件，有一个符合就返回True
            for condition in task.change_conditions:
                if self._evaluate_condition(condition, current_elements, last_elements):
                    if debug:
                        log_monitor_info(f"测试任务变化条件 {condition.element_name} {condition.operator} 触发")
                    else:
                        log_monitor_info(f"任务 {task.name} 变化条件 {condition.element_name} {condition.operator} 触发")
                    return True
            
            # 没有条件触发，检查是否首次运行
            if not last_content:
                if debug:
                    log_monitor_info(f"测试任务首次检查，无基准数据")
                else:
                    log_monitor_info(f"任务 {task.name} 首次检查，建立基准")
                return False
            
            if debug:
                log_monitor_info(f"测试任务所有变化条件均未触发")
            else:
                log_monitor_debug(f"任务 {task.name} 所有变化条件均未触发")
            return False
            
        finally:
            # 只在非调试模式下更新数据库中的内容
            if not debug:
                full_content = {
                    'elements': current_results['elements'],
                    'formatted_message': current_results.get('formatted_message', '')
                }
                task.last_content = json.dumps(full_content, sort_keys=True, ensure_ascii=False)

    def _evaluate_condition(self, condition, current_elements, last_elements):
        """评估单个变化条件
        
        Args:
            condition: 变化条件对象
            current_elements: 当前元素值字典
            last_elements: 上次元素值字典
            
        Returns:
            bool: 条件是否满足
        """
        element_name = condition.element_name
        operator = condition.operator
        compare_value = condition.compare_value
        
        current_value = current_elements.get(element_name)
        last_value = last_elements.get(element_name)
        
        # 如果当前值为None或空，大部分条件都不满足
        if current_value is None or current_value == '':
            return False
        
        current_str = str(current_value).strip()
        
        try:
            if operator == 'contains':
                return compare_value in current_str
            
            elif operator == 'not_contains':
                return compare_value not in current_str
            
            elif operator == 'greater_than':
                try:
                    current_num = float(current_str)
                    compare_num = float(compare_value)
                    return current_num > compare_num
                except (ValueError, TypeError):
                    return False
            
            elif operator == 'less_than':
                try:
                    current_num = float(current_str)
                    compare_num = float(compare_value)
                    return current_num < compare_num
                except (ValueError, TypeError):
                    return False
            
            elif operator == 'increased':
                if last_value is None:
                    return False
                try:
                    current_num = float(current_str)
                    last_num = float(str(last_value).strip())
                    if compare_value:
                        # 指定了变化幅度，检查是否增加了指定的数值
                        threshold = float(compare_value)
                        return current_num >= last_num + threshold
                    else:
                        # 未指定变化幅度，只要增加就算
                        return current_num > last_num
                except (ValueError, TypeError):
                    return False
            
            elif operator == 'decreased':
                if last_value is None:
                    return False
                try:
                    current_num = float(current_str)
                    last_num = float(str(last_value).strip())
                    if compare_value:
                        # 指定了变化幅度，检查是否减少了指定的数值
                        threshold = float(compare_value)
                        return current_num <= last_num - threshold
                    else:
                        # 未指定变化幅度，只要减少就算
                        return current_num < last_num
                except (ValueError, TypeError):
                    return False
            
            else:
                log_monitor_warning(f"未知的变化条件操作符: {operator}")
                return False
                
        except Exception as e:
            log_monitor_error(f"评估变化条件时出错: {e}")
            return False
            
    def _get_last_content(self, task):
        """获取任务的上次内容
        
        Args:
            task: 任务对象
            
        Returns:
            dict or None: 上次解析的内容字典，如果没有则返回None
        """
        try:
            if task.last_content:
                return json.loads(task.last_content)
            return None
        except json.JSONDecodeError as e:
            log_monitor_error(f"解析任务 {task.name} 的上次内容失败: {e}")
            return None
        except Exception as e:
            log_monitor_error(f"获取任务 {task.name} 的上次内容时出错: {e}")
            return None
            
    def _update_task_status(self, task, success, response_time, error):
        """更新任务状态"""
        try:
            task.last_check = datetime.utcnow()
            task.last_response_time = response_time
            
            if success:
                task.last_status = 200
                task.consecutive_errors = 0
                task.last_error = None
            else:
                task.last_status = 500
                task.error_count = (task.error_count or 0) + 1
                task.consecutive_errors = (task.consecutive_errors or 0) + 1
                task.last_error = error
                
            db.session.commit()
            
        except Exception as e:
            log_monitor_error(f"更新任务状态时出错: {e}")
            db.session.rollback()
            
    def _handle_error(self, task, error_msg, response_time):
        """处理错误"""
        log_monitor_error(f"任务 {task.name} 出错: {error_msg}")
        self._update_task_status(task, False, response_time, error_msg)
        
    def _send_notifications(self, task, results):
        """发送通知"""
        try:
            message = self._build_notification_message(task, results)
            
            for notification in task.notifications:
                try:
                    # 使用工厂模式发送通知
                    result = NotificationSenderFactory.send_notification(notification, task, message)
                    
                    if result['success']:
                        log_monitor_info(f"通知发送成功 {notification.name}: {result.get('message', '成功')}")
                    else:
                        log_monitor_error(f"通知发送失败 {notification.name}: {result.get('error', '未知错误')}", task_id=task.id, task_name=task.name)
                        
                except Exception as e:
                    log_monitor_error(f"发送通知异常 {notification.name}: {e}", task_id=task.id, task_name=task.name)
                    
        except Exception as e:
            log_monitor_error(f"发送通知时出错: {e}")
            
    def _build_notification_message(self, task, results):
        """构建通知消息"""
        message = ""
        # 使用预先替换好的消息
        if results.get('formatted_message'):
            message += f"{results['formatted_message']}\n"
        elif task.message:
            message += f"{task.message}\n"
                
        return message

    def _replace_template_placeholders(self, task, elements):
        """替换模板中的占位符
        
        Args:
            task: 任务对象
            elements: 提取的元素值字典
            
        Returns:
            str: 替换后的消息，如果没有消息模板则使用默认模板
        """
        # 如果没有设置消息模板，使用默认模板
        if not task.message:
            if not elements:
                return None
            # 默认模板：用制表符连接所有变量，格式为"键名:值"
            formatted_pairs = []
            for key, value in elements.items():
                safe_value = str(value) if value is not None else ''
                formatted_pairs.append(f"{key}:{safe_value}")
            return '\t'.join(formatted_pairs)
            
        try:
            # 创建一个安全的替换字典，将None值转换为空字符串
            safe_elements = {}
            for key, value in elements.items():
                safe_elements[key] = str(value) if value is not None else ''
            
            # 使用Python的字符串格式化替换占位符
            formatted_message = task.message.format(**safe_elements)
            return formatted_message
            
        except KeyError as e:
            # 如果模板中引用了不存在的元素，记录警告并返回原模板
            missing_key = str(e).strip("'\"")
            log_monitor_warning(f"模板中引用了不存在的元素: {missing_key}")
            return task.message
        except Exception as e:
            log_monitor_error(f"模板替换时发生错误: {e}")
            return task.message


# 全局监控服务单实例
monitor_service = MonitorService()
