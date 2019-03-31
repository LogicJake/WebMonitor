#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-31 10:45:15
@LastEditTime: 2019-03-31 12:38:06
'''
import unittest
from app.main.rule import is_changed


class TestRule(unittest.TestCase):
    def test_last_content_empty(self):
        rule = ''
        content = '变化'
        last_content = ''
        res = is_changed(rule, content, last_content)
        self.assertTrue(res)

    def test_no_rule(self):
        rule = ''
        content = '变化'
        last_content = '变化'
        res = is_changed(rule, content, last_content)
        self.assertFalse(res)

        rule = ''
        content = '变化'
        last_content = '不变化'
        res = is_changed(rule, content, last_content)
        self.assertTrue(res)

    def test_contains(self):
        rule = '-contain 变化'
        content = '变化'
        last_content = '不变化'
        res = is_changed(rule, content, last_content)
        self.assertTrue(res)

        rule = '-contain 变化'
        content = '你好'
        last_content = '不变化'
        res = is_changed(rule, content, last_content)
        self.assertFalse(res)

    def test_increase(self):
        rule = '-increase 3'
        content = '1888.1'
        last_content = '1885.1'
        res = is_changed(rule, content, last_content)
        self.assertFalse(res)

        rule = '-increase 3'
        content = '1888.2'
        last_content = '1885.1'
        res = is_changed(rule, content, last_content)
        self.assertTrue(res)

        rule = '-increase 0'
        content = '1888.1'
        last_content = '1888.1'
        res = is_changed(rule, content, last_content)
        self.assertFalse(res)

        rule = '-increase 0'
        content = '1888.2'
        last_content = '1888.1'
        res = is_changed(rule, content, last_content)
        self.assertTrue(res)

    def test_decrease(self):
        rule = '-decrease 3'
        content = '1882.1'
        last_content = '1885.1'
        res = is_changed(rule, content, last_content)
        self.assertFalse(res)

        rule = '-decrease 3'
        content = '1882'
        last_content = '1885.1'
        res = is_changed(rule, content, last_content)
        self.assertTrue(res)

        rule = '-decrease 0'
        content = '1888.1'
        last_content = '1888.1'
        res = is_changed(rule, content, last_content)
        self.assertFalse(res)

        rule = '-decrease 0'
        content = '1888.0'
        last_content = '1888.1'
        res = is_changed(rule, content, last_content)
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()
