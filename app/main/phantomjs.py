#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:52:35
@LastEditTime: 2019-03-24 21:20:25
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from lxml import etree
import warnings

warnings.filterwarnings("ignore")


class PhantomJS():
    def get_by_xpath(self, url, xpath):
        driver = webdriver.PhantomJS()
        driver.get(url)

        html = driver.page_source
        s = etree.HTML(html)
        res = None

        try:
            content = s.xpath(xpath)
            if len(content) != 0:
                res = content[0]
        except Exception as e:
            # driver.save_screenshot()
            raise Exception('获取不到文本信息')

        driver.close()
        return res


if __name__ == "__main__":
    phantomjs = PhantomJS()
    phantomjs.get_by_xpath('https://www.baidu.com/',
                           '//*[@id="su"]/@value')
