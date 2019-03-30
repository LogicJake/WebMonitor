#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:52:35
@LastEditTime: 2019-03-30 15:06:10
'''
import ast
import warnings

from scrapy.selector import Selector
from selenium import webdriver

from app.main.selector.selector import Selector as FatherSelector

warnings.filterwarnings("ignore")


class PhantomJSSelector(FatherSelector):
    def __init__(self, debug=False):
        self.debug = debug

    def get_html(self, url, headers):
        # 默认userAgent
        webdriver.DesiredCapabilities.PHANTOMJS[
            'phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'

        if headers:
            header_dict = ast.literal_eval(headers)
            if type(header_dict) != dict:
                raise Exception('必须是字典格式')

            for key, value in header_dict.items():
                if key.lower() == 'User-Agent':
                    webdriver.DesiredCapabilities.PHANTOMJS[
                        'phantomjs.page.settings.userAgent'] = value
                else:
                    webdriver.DesiredCapabilities.PHANTOMJS[
                        'phantomjs.page.customHeaders.{}'.format(key)] = value

        driver = webdriver.PhantomJS()
        driver.get(url)
        if self.debug:
            import os
            basepath = os.path.dirname(os.path.dirname(__file__))
            save_path = os.path.join(basepath, '..', 'static', 'error')
            os.makedirs(save_path, exist_ok=True)
            driver.save_screenshot(os.path.join(save_path, 'screenshot.png'))
        html = driver.page_source
        driver.close()
        return html

    def get_by_xpath(self, url, xpath, headers=None):
        html = self.get_html(url, headers)
        res = Selector(text=html).xpath(xpath).extract()

        if len(res) != 0:
            return res[0]
        else:
            raise Exception('无法获取文本信息')

    def get_by_css(self, url, xpath, headers=None):
        html = self.get_html(url, headers)
        res = Selector(text=html).css(xpath).extract()

        if len(res) != 0:
            return res[0]
        else:
            raise Exception('无法获取文本信息')
