#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-25 12:31:35
@LastEditTime: 2019-03-26 16:18:16
'''
import requests
from lxml import etree

from app.main.selector.selector import Selector


class RequestsSelector(Selector):
    def get_by_xpath(self, url, xpath):
        r = requests.get(url, timeout=10)
        html = r.text
        s = etree.HTML(html)
        res = None

        content = s.xpath(xpath)

        if len(content) != 0:
            res = content[0]
            if type(res) == etree._Element:
                res = res.text
        else:
            raise Exception('无法获取文本信息')

        return res
