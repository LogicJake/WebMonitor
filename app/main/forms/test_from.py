import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


def check_url(form, field):
    url = form.url.data
    try:
        requests.get(url, timeout=10)
    except Exception as e:
        raise ValidationError(repr(e))


class TestForm(FlaskForm):
    url = StringField('监控网址', validators=[DataRequired("请输入网址!"), check_url])
    selector_type = SelectField(
        '元素选择器类型', choices=[('xpath', 'xpath'), ('css', 'css selector'), ('json', 'Jsonpath')])
    selector = StringField('元素选择器', validators=[DataRequired("请输入元素选择器!")])
    is_chrome = SelectField(
        '是否使用无头浏览器', choices=[('no', 'no'), ('yes', 'yes')])
    regular_expression = StringField('正则表达式')
    headers = StringField('自定义请求头')
    submit = SubmitField('提取信息')
