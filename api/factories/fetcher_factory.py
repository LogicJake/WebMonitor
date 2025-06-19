"""
网页抓取器工厂类
提供统一的网页抓取接口，支持requests和Playwright两种方式
"""

import time
import json
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from api.services.log_service import log_monitor_info, log_monitor_warning, log_monitor_error

# 尝试导入Playwright
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    log_monitor_warning("Playwright未安装，无法使用浏览器模式")


class BaseFetcher(ABC):
    """网页抓取器基类"""
    
    @abstractmethod
    def fetch(self, url: str, custom_headers: Optional[Dict] = None, timeout: int = 30) -> Dict[str, Any]:
        """
        抓取网页内容
        
        Args:
            url: 目标URL
            custom_headers: 自定义请求头
            timeout: 超时时间（秒）
        
        Returns:
            包含响应信息的字典
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查抓取器是否可用"""
        pass


class RequestsFetcher(BaseFetcher):
    """基于requests的网页抓取器"""
    
    def fetch(self, url: str, custom_headers: Optional[Dict] = None, timeout: int = 30) -> Dict[str, Any]:
        """使用requests抓取网页内容"""
        try:
            log_monitor_info(f"使用requests抓取: {url}")
            
            start_time = time.time()
            
            # 构建请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 添加自定义请求头
            if custom_headers:
                try:
                    if isinstance(custom_headers, str):
                        custom_headers = json.loads(custom_headers)
                    if isinstance(custom_headers, dict):
                        headers.update(custom_headers)
                        log_monitor_info(f"添加自定义请求头: {list(custom_headers.keys())}")
                except (json.JSONDecodeError, TypeError) as e:
                    log_monitor_warning(f"解析自定义请求头失败: {e}")
            
            # 发送HTTP请求
            response = requests.get(
                url,
                timeout=timeout,
                headers=headers,
                allow_redirects=True
            )
            
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                return {
                    'success': False,
                    'content': None,
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'error': f"HTTP错误: {response.status_code}",
                    'url': response.url,
                    'headers': dict(response.headers)
                }
            
            log_monitor_info(f"requests抓取成功，响应时间: {response_time:.3f}s")
            
            return {
                'success': True,
                'content': response.text,
                'status_code': response.status_code,
                'response_time': response_time,
                'error': None,
                'url': response.url,
                'headers': dict(response.headers)
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'content': None,
                'status_code': None,
                'response_time': timeout,
                'error': "请求超时"
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'content': None,
                'status_code': None,
                'response_time': 0,
                'error': "连接失败"
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'content': None,
                'status_code': None,
                'response_time': 0,
                'error': f"请求异常: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'content': None,
                'status_code': None,
                'response_time': 0,
                'error': f"未知错误: {str(e)}"
            }
    
    def is_available(self) -> bool:
        """requests总是可用的"""
        return True


class PlaywrightFetcher(BaseFetcher):
    """基于Playwright的网页抓取器"""
    
    def fetch(self, url: str, custom_headers: Optional[Dict] = None, timeout: int = 30) -> Dict[str, Any]:
        """使用Playwright抓取网页内容"""
        if not self.is_available():
            return {
                'success': False,
                'content': None,
                'status_code': None,
                'response_time': 0,
                'error': f"Playwright未安装，请运行: {self.get_installation_command()}"
            }
        
        try:
            log_monitor_info(f"使用Playwright抓取: {url}")
            
            start_time = time.time()
            
            # 解析自定义请求头
            headers = {}
            if custom_headers:
                try:
                    if isinstance(custom_headers, str):
                        headers = json.loads(custom_headers)
                    elif isinstance(custom_headers, dict):
                        headers = custom_headers
                    log_monitor_info(f"添加自定义请求头: {list(headers.keys())}")
                except (json.JSONDecodeError, TypeError) as e:
                    log_monitor_warning(f"解析自定义请求头失败: {e}")
            
            # 使用Playwright抓取
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-features=VizDisplayCompositor'
                    ]
                )
                
                try:
                    page = browser.new_page()
                    
                    # 设置超时
                    timeout_ms = timeout * 1000
                    page.set_default_timeout(timeout_ms)
                    page.set_default_navigation_timeout(timeout_ms)
                    
                    # 设置用户代理和请求头
                    extra_headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    }
                    extra_headers.update(headers)
                    page.set_extra_http_headers(extra_headers)
                    
                    # 访问页面，等待网络空闲
                    response = page.goto(url, wait_until='networkidle')
                    
                    if not response:
                        raise Exception("页面响应为空")
                    
                    # 等待页面完全加载
                    page.wait_for_load_state('networkidle')
                    
                    # 获取页面内容
                    content = page.content()
                    response_time = time.time() - start_time
                    
                    log_monitor_info(f"Playwright抓取成功，响应时间: {response_time:.3f}s")
                    
                    return {
                        'success': True,
                        'content': content,
                        'status_code': response.status,
                        'response_time': response_time,
                        'error': None,
                        'url': response.url,
                        'headers': dict(response.headers)
                    }
                    
                finally:
                    browser.close()
                    
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = str(e)
            log_monitor_error(f"Playwright抓取失败: {error_msg}")
            
            return {
                'success': False,
                'content': None,
                'status_code': None,
                'response_time': response_time,
                'error': f"Playwright异常: {error_msg}"
            }
    
    def is_available(self) -> bool:
        """检查Playwright是否可用"""
        return PLAYWRIGHT_AVAILABLE
    
    @staticmethod
    def get_installation_command() -> str:
        """获取安装命令"""
        return "pip install playwright && playwright install chromium"


class FetcherFactory:
    """网页抓取器工厂类"""
    
    _fetchers = {
        'requests': RequestsFetcher(),
        'playwright': PlaywrightFetcher()
    }
    
    @classmethod
    def get_fetcher(cls, fetcher_type: str) -> BaseFetcher:
        """
        获取指定类型的抓取器
        
        Args:
            fetcher_type: 抓取器类型 ('requests' 或 'playwright')
        
        Returns:
            抓取器实例
        
        Raises:
            ValueError: 不支持的抓取器类型
        """
        if fetcher_type not in cls._fetchers:
            raise ValueError(f"不支持的抓取器类型: {fetcher_type}")
        
        fetcher = cls._fetchers[fetcher_type]
        if not fetcher.is_available():
            if fetcher_type == 'playwright':
                raise RuntimeError(f"Playwright不可用，请运行: {PlaywrightFetcher.get_installation_command()}")
            else:
                raise RuntimeError(f"抓取器 {fetcher_type} 不可用")
        
        return fetcher
    
    @classmethod
    def fetch_webpage(cls, url: str, use_playwright: bool = False, custom_headers: Optional[Dict] = None, timeout: int = 30) -> Dict[str, Any]:
        """
        统一的网页抓取接口
        
        Args:
            url: 目标URL
            use_playwright: 是否使用Playwright
            custom_headers: 自定义请求头
            timeout: 超时时间（秒）
        
        Returns:
            包含响应信息的字典
        """
        fetcher_type = 'playwright' if use_playwright else 'requests'
        
        try:
            fetcher = cls.get_fetcher(fetcher_type)
            return fetcher.fetch(url, custom_headers, timeout)
        except (ValueError, RuntimeError) as e:
            log_monitor_error(f"获取抓取器失败: {e}")
            return {
                'success': False,
                'content': None,
                'status_code': None,
                'response_time': 0,
                'error': str(e)
            }
    
    @classmethod
    def register_fetcher(cls, name: str, fetcher: BaseFetcher):
        """
        注册新的抓取器
        
        Args:
            name: 抓取器名称
            fetcher: 抓取器实例
        """
        cls._fetchers[name] = fetcher
    
    @classmethod
    def get_available_fetchers(cls) -> Dict[str, bool]:
        """
        获取所有抓取器的可用状态
        
        Returns:
            抓取器名称和可用状态的字典
        """
        return {name: fetcher.is_available() for name, fetcher in cls._fetchers.items()}


# 使用示例
if __name__ == "__main__":
    # 测试requests抓取器
    result = FetcherFactory.fetch_webpage("https://httpbin.org/get", use_playwright=False)
    print("Requests结果:", result['success'])
    
    # 测试Playwright抓取器（如果可用）
    if PLAYWRIGHT_AVAILABLE:
        result = FetcherFactory.fetch_webpage("https://httpbin.org/get", use_playwright=True)
        print("Playwright结果:", result['success'])
    
    # 查看可用的抓取器
    print("可用抓取器:", FetcherFactory.get_available_fetchers()) 