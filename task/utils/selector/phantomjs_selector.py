import ast
import warnings
from collections import OrderedDict

from selenium import webdriver
from task.utils.selector.selector import SelectorABC as FatherSelector

warnings.filterwarnings("ignore")

USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'


class PhantomJSSelector(FatherSelector):
    def __init__(self, debug=False):
        self.debug = debug

    def get_html(self, url, headers):
        # 默认userAgent
        webdriver.DesiredCapabilities.PHANTOMJS[
            'phantomjs.page.settings.userAgent'] = USERAGENT

        if headers:
            header_dict = ast.literal_eval(headers)
            if type(header_dict) != dict:
                raise Exception('必须是字典格式')

            for key, value in header_dict.items():
                if key.lower() == 'User-Agent':
                    webdriver.DesiredCapabilities.PHANTOMJS[
                        'phantomjs.page.settings.userAgent'] = value
                else:
                    webdriver.DesiredCapabilities.PHANTOMJS[
                        'phantomjs.page.customHeaders.{}'.format(key)] = value

        driver = webdriver.PhantomJS()
        driver.get(url)
        if self.debug:
            import os
            basepath = os.path.dirname(os.path.dirname(__file__))
            save_path = os.path.join(basepath, '..', 'static', 'error')
            os.makedirs(save_path, exist_ok=True)
            driver.save_screenshot(os.path.join(save_path, 'screenshot.png'))
        html = driver.page_source
        driver.quit()
        return html

    def get_by_xpath(self, url, selector_dict, headers=None):
        html = self.get_html(url, headers)

        result = OrderedDict()
        for key, xpath_ext in selector_dict.items():
            result[key] = self.xpath_parse(html, xpath_ext)

        return result

    def get_by_css(self, url, selector_dict, headers=None):
        html = self.get_html(url, headers)

        result = OrderedDict()
        for key, css_ext in selector_dict.items():
            result[key] = self.css_parse(html, css_ext)

        return result
