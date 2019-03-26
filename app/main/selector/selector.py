#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-25 12:23:59
@LastEditTime: 2019-03-26 16:45:34
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
