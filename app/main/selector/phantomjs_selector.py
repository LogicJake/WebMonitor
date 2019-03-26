#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:52:35
@LastEditTime: 2019-03-26 16:19:42
'''
import warnings

from lxml import etree
from selenium import webdriver

from app.main.selector.selector import Selector

warnings.filterwarnings("ignore")


class PhantomJSSelector(Selector):
    def get_by_xpath(self, url, xpath):
        driver = webdriver.PhantomJS()
        driver.get(url)

        html = driver.page_source
        s = etree.HTML(html)
        res = None

        content = s.xpath(xpath)

        if len(content) != 0:
            res = content[0]
            if type(res) == etree._Element:
                res = res.text
        else:
            raise Exception('无法获取文本信息')

        driver.close()
        return res
