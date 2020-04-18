#!/usr/bin/env python
# coding=UTF-8
'''
@Author: LogicJake
@Date: 2019-03-25 12:27:44
@LastEditTime: 2019-03-30 15:59:08
'''
from task.utils.selector.phantomjs_selector import PhantomJSSelector
from task.utils.selector.request_selector import RequestsSelector


def new_handler(name, debug=False):
    if name == 'request':
        return RequestsSelector(debug)
    elif name == 'phantomjs':
        return PhantomJSSelector(debug)
    else:
        raise Exception()
