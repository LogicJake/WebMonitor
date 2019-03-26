from app.main.selector.selector_handler import new_handler
import re


def extract_by_re(conetnt, regular_expression):
    m = re.match(regular_expression, conetnt)

    if m:
        return m.groups()[0]
    else:
        raise Exception('无法使用正则提取')


def get_content(url,
                is_chrome,
                selector_type,
                selector,
                regular_expression=None):
    content = None
    if is_chrome == 'no':
        selector_handler = new_handler('request')

        if selector_type == 'xpath':
            content = selector_handler.get_by_xpath(url, selector)
        elif selector_type == 'css':
            content = selector_handler.get_by_css(url, selector)
        else:
            raise Exception('无效选择器')
    else:
        selector_handler = new_handler('phantomjs')

        if selector_type == 'xpath':
            content = selector_handler.get_by_xpath(url, selector)
        elif selector_type == 'css':
            content = selector_handler.get_by_css(url, selector)
        else:
            raise Exception('无效选择器')

    if regular_expression:
        content = extract_by_re(content, regular_expression)
    return content
