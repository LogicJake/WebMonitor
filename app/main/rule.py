def is_changed(rule, content, last_content):
    if not last_content:
        return True
    else:
        if not rule:
            if last_content != content:
                return True
    return False
