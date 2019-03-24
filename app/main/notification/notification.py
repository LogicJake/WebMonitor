#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-24 20:24:33
@LastEditTime: 2019-03-24 20:25:59
'''
from abc import ABCMeta, abstractmethod


class Notification():
    __metaclass__ = ABCMeta

    @abstractmethod
    def send(self):
        pass
