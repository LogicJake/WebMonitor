#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:52:35
@LastEditTime: 2019-03-27 09:56:26
'''
import warnings

from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from app.main.selector.selector import Selector as FatherSelector

warnings.filterwarnings("ignore")


class PhantomJSSelector(FatherSelector):
    def get_html(self, url):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        )
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
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
