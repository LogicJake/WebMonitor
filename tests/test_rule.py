import unittest
from task.utils.rule import is_changed


class TestRule(unittest.TestCase):
    def test_last_content_empty(self):
        rule = ''
        content = '变化'
        last_content = ''
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 3)

    def test_no_rule(self):
        rule = ''
        content = '变化'
        last_content = '变化'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 0)

        rule = ''
        content = '变化'
        last_content = '不变化'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 3)

    def test_contains(self):
        rule = '-contain 变化'
        content = '变化'
        last_content = '不变化'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 2)

        rule = '-contain 变化'
        content = '你好'
        last_content = '不变化'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 1)

    def test_increase(self):
        rule = '-increase 3'
        content = '1888.1'
        last_content = '1885.1'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 1)

        rule = '-increase 3'
        content = '1888.2'
        last_content = '1885.1'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 2)

        rule = '-increase 0'
        content = '1888.1'
        last_content = '1888.1'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 0)

        rule = '-increase 0'
        content = '1888.2'
        last_content = '1888.1'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 2)

    def test_decrease(self):
        rule = '-decrease 3'
        content = '1882.1'
        last_content = '1885.1'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 1)

        rule = '-decrease 3'
        content = '1882'
        last_content = '1885.1'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 2)

        rule = '-decrease 0'
        content = '1888.1'
        last_content = '1888.1'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 0)

        rule = '-decrease 0'
        content = '1888.0'
        last_content = '1888.1'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 2)

    def test_equal(self):
        rule = '-equal 3'
        content = '3.1'
        last_content = '2'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 1)

        rule = '-equal 3'
        content = '3'
        last_content = '2'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 2)

        rule = '-equal 3'
        content = '3'
        last_content = '3'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 0)

    def test_less(self):
        rule = '-less 3'
        content = '3'
        last_content = '2'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 1)

        rule = '-less 3'
        content = '2.9'
        last_content = '2'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 2)

        rule = '-less 3.1'
        content = '3'
        last_content = '3'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 0)

    def test_more(self):
        rule = '-more 3'
        content = '3'
        last_content = '2'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 1)

        rule = '-more 3'
        content = '3.1'
        last_content = '2'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 2)

        rule = '-more 2.9'
        content = '3'
        last_content = '3'
        res = is_changed(rule, content, last_content)
        self.assertEqual(res, 0)


if __name__ == '__main__':
    unittest.main()
