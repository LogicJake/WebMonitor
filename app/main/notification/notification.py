#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 20:24:33
@LastEditTime: 2019-03-25 18:59:56
'''
from abc import ABCMeta, abstractmethod


class Notification():
    __metaclass__ = ABCMeta

    @abstractmethod
    def send(self, to, header, content):
        pass
