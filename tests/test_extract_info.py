import unittest
from task.utils.extract_info import extract_by_re


class TestExtract(unittest.TestCase):
    def test_re1(self):
        regular_expression = r'([1-9]\d*)'
        content = '价格：1390'
        res = extract_by_re(content, regular_expression)
        self.assertEqual(res, '1390')

    def test_re2(self):
        regular_expression = r'([1-9]\d*)'
        content = '1391好贵'
        res = extract_by_re(content, regular_expression)
        self.assertEqual(res, '1391')


if __name__ == '__main__':
    unittest.main()
