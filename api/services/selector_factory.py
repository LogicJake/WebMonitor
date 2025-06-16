"""
选择器解析器工厂模块

提供各种类型的选择器解析器，支持动态注册新的解析器类型。
"""

import json
from abc import ABC, abstractmethod
from lxml import html
from jsonpath import jsonpath


class SelectorParser(ABC):
    """选择器解析器基类"""
    
    @abstractmethod
    def parse(self, content, expression):
        """解析内容
        
        Args:
            content: 网页内容
            expression: 选择器表达式
            
        Returns:
            str or None: 解析结果
        """
        pass


class XPathParser(SelectorParser):
    """XPath选择器解析器"""
    
    def parse(self, content, expression):
        try:
            tree = html.fromstring(content)
            elements = tree.xpath(expression)
            if elements:
                if hasattr(elements[0], 'text_content'):
                    return elements[0].text_content().strip()
                else:
                    return str(elements[0]).strip()
            return None
        except Exception as e:
            raise ValueError(f"XPath解析错误: {e}")


class CSSParser(SelectorParser):
    """CSS选择器解析器"""
    
    def parse(self, content, expression):
        try:
            tree = html.fromstring(content)
            elements = tree.cssselect(expression)
            if elements:
                return elements[0].text_content().strip()
            return None
        except Exception as e:
            raise ValueError(f"CSS选择器解析错误: {e}")


class JSONPathParser(SelectorParser):
    """JSONPath选择器解析器"""
    
    def parse(self, content, expression):
        try:
            json_data = json.loads(content)
            matches = jsonpath(json_data, expression)
            if matches:
                return str(matches[0])
            return None
        except json.JSONDecodeError:
            raise ValueError("JSONPath需要JSON格式响应")
        except Exception as e:
            raise ValueError(f"JSONPath解析错误: {e}")

class BeautifulSoupParser(SelectorParser):
    """BeautifulSoup选择器解析器"""
    
    def parse(self, content, expression):
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # 支持CSS选择器语法
            element = soup.select_one(expression)
            if element:
                return element.get_text().strip()
            return None
        except ImportError:
            raise ValueError("BeautifulSoup解析器需要安装 beautifulsoup4")
        except Exception as e:
            raise ValueError(f"BeautifulSoup解析错误: {e}")


class SelectorParserFactory:
    """选择器解析器工厂"""
    
    _parsers = {
        'xpath': XPathParser(),
        'css': CSSParser(),
        'jsonpath': JSONPathParser(),
        'bs4': BeautifulSoupParser(),
    }
    
    @classmethod
    def get_parser(cls, selector_type):
        """获取选择器解析器
        
        Args:
            selector_type: 选择器类型
            
        Returns:
            SelectorParser: 对应的解析器实例
            
        Raises:
            ValueError: 不支持的选择器类型
        """
        parser = cls._parsers.get(selector_type.lower())
        if not parser:
            raise ValueError(f"不支持的选择器类型: {selector_type}")
        return parser
    
    @classmethod
    def register_parser(cls, selector_type, parser):
        """注册新的选择器解析器
        
        Args:
            selector_type: 选择器类型名称
            parser: 解析器实例
            
        Raises:
            TypeError: 解析器类型错误
        """
        if not isinstance(parser, SelectorParser):
            raise TypeError("解析器必须继承自SelectorParser")
        cls._parsers[selector_type.lower()] = parser
    
    @classmethod
    def unregister_parser(cls, selector_type):
        """注销选择器解析器
        
        Args:
            selector_type: 选择器类型名称
            
        Returns:
            bool: 是否成功注销
        """
        return cls._parsers.pop(selector_type.lower(), None) is not None
    
    @classmethod
    def get_supported_types(cls):
        """获取支持的选择器类型列表
        
        Returns:
            list: 支持的选择器类型列表
        """
        return list(cls._parsers.keys())
    
    @classmethod
    def is_supported(cls, selector_type):
        """检查是否支持指定的选择器类型
        
        Args:
            selector_type: 选择器类型
            
        Returns:
            bool: 是否支持
        """
        return selector_type.lower() in cls._parsers


# 使用示例和扩展指南
"""
如何添加新的选择器类型：

1. 创建解析器类：
class CustomParser(SelectorParser):
    def parse(self, content, expression):
        # 实现自定义解析逻辑
        try:
            # 解析逻辑
            result = your_parsing_logic(content, expression)
            return result
        except Exception as e:
            raise ValueError(f"自定义解析错误: {e}")

2. 注册解析器：
SelectorParserFactory.register_parser('custom', CustomParser())

3. 使用：
parser = SelectorParserFactory.get_parser('custom')
result = parser.parse(content, expression)

支持的选择器类型：
- xpath: XPath选择器
- css: CSS选择器
- jsonpath: JSONPath选择器
- regex: 正则表达式
- bs4: BeautifulSoup选择器（需要安装beautifulsoup4）
""" 