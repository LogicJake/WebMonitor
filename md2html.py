import markdown


class Markdown2Html:
    def convert(self, infile, outfile):
        with open(infile, 'r', encoding='utf8') as f:
            markdownText = f.read()

        raw_html = markdown.markdown(
            markdownText, output_format='html5', extensions=['extra'])

        css = '<link href="../../static/css/github.css" rel="stylesheet" type="text/css"/>\n'

        tip = '<p>点击<a target="_blank" href="/login">此处</a>登录，如果你是刚初始化项目，则账户名为admin，密码在日志文件中，请登录之后及时修改密码！</p>\n'

        template_html = "{% extends 'admin/master.html' %}\
            \n{% block body %}\n" + css + tip + raw_html + '\n{% endblock %}'

        with open(outfile, 'w', encoding='utf8') as f:
            f.write(template_html)
