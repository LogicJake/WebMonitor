def parse_contain(args, content, last_content):
    '''
    新内容中是否包含某个字符串
    -contain 上架
    '''
    try:
        key_index = args.index('-contain')
    except ValueError:
        return True

    value_index = key_index + 1
    value = args[value_index]

    if value in content:
        return True
    return False


def parse_increase(args, content, last_content):
    '''
    相较于旧值，数值增长超过阈值
    -increase 3
    content, last_content和参数值都应该为数值型，否则会抛出异常
    '''
    try:
        key_index = args.index('-increase')
    except ValueError:
        return True

    value_index = key_index + 1
    value = args[value_index]

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
    try:
        key_index = args.index('-decrease')
    except ValueError:
        return True

    value_index = key_index + 1
    value = args[value_index]

    last_content = float(last_content)
    content = float(content)
    value = float(value)

    if content < last_content and last_content - content > value:
        return True
    return False


rule_funs = [parse_contain, parse_increase, parse_decrease]


def is_changed(rule, content, last_content):
    if last_content:
        if last_content == content:
            return False
        else:
            if rule:
                args = rule.split(' ')
                for rule_fun in rule_funs:
                    if not rule_fun(args, content, last_content):
                        return False
    return True
