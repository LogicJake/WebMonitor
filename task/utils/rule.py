def parse_contain(args, content, last_content):
    '''
    新内容中是否包含某个字符串
    -contain 上架
    '''
    if args[0] != '-contain':
        return False

    value = args[1]

    if value in content:
        return True
    return False


def parse_increase(args, content, last_content):
    '''
    相较于旧值，数值增长超过阈值
    -increase 3
    content, last_content和参数值都应该为数值型，否则会抛出异常
    '''
    if args[0] != '-increase':
        return False

    if last_content == '':
        return False

    value = args[1]

    last_content = float(last_content)
    content = float(content)
    value = float(value)

    if content > last_content and content - last_content > value:
        return True
    return False


def parse_decrease(args, content, last_content):
    '''
    相较于旧值，数值减少超过阈值
    -decrease 3
    content, last_content和参数值都应该为数值型，否则会抛出异常
    '''
    if args[0] != '-decrease':
        return False

    if last_content == '':
        return False

    value = args[1]

    last_content = float(last_content)
    content = float(content)
    value = float(value)

    if content < last_content and last_content - content > value:
        return True
    return False


def parse_equal(args, content, last_content):
    '''
    数值等于某个值
    -equal 3
    content和参数值都应该为数值型，否则会抛出异常
    '''
    if args[0] != '-equal':
        return False

    value = args[1]

    content = float(content)
    value = float(value)

    if content == value:
        return True
    return False


def parse_less(args, content, last_content):
    '''
    数值小于某个值
    -less 3
    content和参数值都应该为数值型，否则会抛出异常
    '''
    if args[0] != '-less':
        return False

    value = args[1]

    content = float(content)
    value = float(value)

    if content < value:
        return True
    return False


def parse_more(args, content, last_content):
    '''
    数值大于某个值
    -less 3
    content和参数值都应该为数值型，否则会抛出异常
    '''
    if args[0] != '-more':
        return False

    value = args[1]

    content = float(content)
    value = float(value)

    if content > value:
        return True
    return False


rule_funs = [
    parse_contain, parse_increase, parse_decrease, parse_equal, parse_less,
    parse_more
]


# 0 无变化(不发送)
# 1 有变化但没有触发规则(更新content 但不发送)
# 2 有变化且触发规则(更新content 发送)
# 3 有变化没有设置规则(更新content 发送)
def is_changed(rules, content, last_content):
    if last_content is not None and last_content == content:
        return 0
    else:
        if rules:
            rules = rules.split(';')
            for rule in rules:
                args = rule.split(' ')
                for rule_fun in rule_funs:
                    if rule_fun(args, content, last_content):
                        return 2
            return 1
        else:
            return 3
