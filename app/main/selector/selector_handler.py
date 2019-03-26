#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-25 12:27:44
@LastEditTime: 2019-03-26 21:39:21
'''
from app.main.selector.phantomjs_selector import PhantomJSSelector
from app.main.selector.request_selector import RequestsSelector


def new_handler(name):
    if name == 'request':
        return RequestsSelector()
    elif name == 'phantomjs':
        return PhantomJSSelector()
    else:
        raise Exception()
