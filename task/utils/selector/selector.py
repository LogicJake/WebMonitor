#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake, Jacob
@Date: 2019-03-25 12:23:59
@LastEditTime: 2020-03-01 14:54:14
'''
from abc import ABCMeta, abstractmethod


class Selector():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_by_xpath(self):
        pass

    @abstractmethod
    def get_by_css(self):
        pass

    @abstractmethod
    def get_by_json(self):
        pass