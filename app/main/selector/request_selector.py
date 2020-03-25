#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake, Jacob
@Date: 2019-03-25 12:31:35
@LastEditTime: 2020-03-01 14:53:38
'''
import ast

import requests
import json
import jsonpath

from scrapy.selector import Selector

from app.main.selector.selector import Selector as FatherSelector


class RequestsSelector(FatherSelector):
    def __init__(self, debug=False):
        self.debug = debug

    def get_html(self, url, headers):
        if headers:
            header_dict = ast.literal_eval(headers)
            if type(header_dict) != dict:
                raise Exception('必须是字典格式')

            r = requests.get(url, headers=header_dict, timeout=10)
        else:
            r = requests.get(url, timeout=10)
        r.encoding = r.apparent_encoding
        html = r.text
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

    def get_by_json(self, url, xpath, headers=None):
        html = self.get_html(url, headers)

        try:
            resJson = json.loads(html)
        except Exception:
            raise Exception('Json转换错误')
        res = jsonpath.jsonpath(resJson, xpath)

        if res:
            if len(res) != 0:
                return res[0]
        else:
            raise Exception('无法获取文本信息')
