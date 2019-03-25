#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 11:52:35
@LastEditTime: 2019-03-25 11:23:18
'''
from selenium import webdriver
from lxml import etree
import warnings
from wtforms.validators import ValidationError
from selenium.common.exceptions import WebDriverException
warnings.filterwarnings("ignore")


class PhantomJS():
    def get_by_xpath(self, url, xpath):
        try:
            driver = webdriver.PhantomJS()
        except WebDriverException as e:
            raise ValidationError(str(e))
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
    phantomjs.get_by_xpath('https://www.baidu.com/', '//*[@id="su"]/@value')
