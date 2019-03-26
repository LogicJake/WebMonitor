#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:52:35
@LastEditTime: 2019-03-26 17:00:35
'''
import warnings

from selenium import webdriver

from app.main.selector.selector import Selector as FatherSelector
from scrapy.selector import Selector

warnings.filterwarnings("ignore")


class PhantomJSSelector(FatherSelector):
    def get_html(self, url):
        driver = webdriver.PhantomJS()
        driver.get(url)
        html = driver.page_source
        driver.close()
        return html

    def get_by_xpath(self, url, xpath):
        html = self.get_html(url)
        res = Selector(text=html).xpath(xpath).extract()

        if len(res) != 0:
            return res[0]
        else:
            raise Exception('无法获取文本信息')

    def get_by_css(self, url, xpath):
        html = self.get_html(url)
        res = Selector(text=html).css(xpath).extract()

        if len(res) != 0:
            return res[0]
        else:
            raise Exception('无法获取文本信息')
