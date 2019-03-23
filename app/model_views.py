from flask_admin.contrib.sqla import ModelView
from wtforms.validators import ValidationError
import requests
from lxml import etree


def check_url(form, field):
    url = form.url.data
    try:
        requests.get(url, timeout=10)
    except Exception as e:
        raise ValidationError(str(e))


def check_selector(form, field):
    selector_type = form.selector_type.data
    selector = form.selector.data
    url = form.url.data

    r = requests.get(url, timeout=10)
    html = r.text

    if selector_type == 'xpath':
        s = etree.HTML(html)
        content = s.xpath(selector)

        if len(content) == 0:
            raise ValidationError('获取不到文本信息，可以尝试选择使用无头浏览器再试一次')


class RecordView(ModelView):
    column_labels = {
        'title': '目标名称',
        'url': '监控网址',
        'create_time': '创建时间',
        'selector_type': '元素选择器类型',
        'selector': '元素选择',
        'is_chrome': '是否使用无头浏览器'
    }
    column_list = ['title', 'url', 'create_time']
    form_args = dict(
        url=dict(validators=[check_url]),
        selector=dict(validators=[check_selector]))
    form_choices = {
        'selector_type': [('xpath', 'xpath'), ('css selector',
                                               'css selector')],
        'is_chrome': [('no', 'no'), ('yes', 'yes')]
    }
