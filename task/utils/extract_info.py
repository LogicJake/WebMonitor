import logging
import re
from collections import OrderedDict

import feedparser
from func_timeout import func_set_timeout
from task.utils.selector.selector_handler import new_handler

logger = logging.getLogger('main')


def extract_by_re(conetnt, regular_expression):
    m = re.search(regular_expression, conetnt)

    if m:
        return m.group(1)
    elif not m:
        return "未检测到相关内容"
    else:
        logger.error('{} 无法使用正则提取'.format(regular_expression))
        raise Exception('无法使用正则提取')


def wrap_template_content(content_dict, content_template):
    if content_template == '':
        content_template = '\t'.join(
            ['{' + k + '}' for k in content_dict.keys()])

    for k, v in content_dict.items():
        content_template = content_template.replace('{' + k + '}', v)

    content = content_template
    return content


def get_content(url,
                is_chrome,
                selector_type,
                selector,
                content_template,
                regular_expression=None,
                headers=None,
                debug=False):
    if is_chrome == 0:
        selector_handler = new_handler('request', debug)
    else:
        selector_handler = new_handler('phantomjs', debug)

    # 兼容旧版本，默认转为{content}
    selector_dict = OrderedDict()
    if '{' not in selector:
        selector_dict['content'] = selector
    else:
        selector_split_list = selector.split('\n')
        for selector_split in selector_split_list:
            selector_split = selector_split.strip()
            key, value = selector_split.split('{')
            value = value.split('}')[0]
            selector_dict[key] = value

    if selector_type == 0:
        content_dict = selector_handler.get_by_xpath(url, selector_dict,
                                                     headers)
    elif selector_type == 1:
        content_dict = selector_handler.get_by_css(url, selector_dict, headers)
    elif selector_type == 2:
        content_dict = selector_handler.get_by_json(url, selector_dict,
                                                    headers)
    else:
        logger.error('无效选择器')
        raise Exception('无效选择器')

    # 添加或替换保留字段：{url}
    if 'url' in content_dict:
        content_dict['url'] = url
    content = wrap_template_content(content_dict, content_template)

    if regular_expression:
        content = extract_by_re(content, regular_expression)
    return content


@func_set_timeout(10)
def get_rss_content(url):
    feeds = feedparser.parse(url)

    if len(feeds.entries) == 0:
        raise Exception('无内容')

    single_post = feeds.entries[0]
    item = {}
    item['title'] = single_post.title
    item['link'] = single_post.link
    item['guid'] = single_post.id

    return item
