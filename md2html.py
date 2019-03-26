import markdown
from bs4 import BeautifulSoup


class Markdown2Html:
    def __init__(self, cssfile):
        with open(cssfile, 'r') as f:
            css = f.read()
            self.headTag = f'<style  type="text/css">{css}</style>'

    def convert(self, infile, outfile):
        with open(infile, 'r', encoding='utf8') as f:
            markdownText = f.read()

        raw_html = self.headTag + markdown.markdown(
            markdownText, output_format='html5', extensions=['extra'])

        template_html = "{% extends 'admin/master.html' %}\n{% block body %}\n" + raw_html + '\n{% endblock %}'

        with open(outfile, 'w', encoding='utf8') as f:
            f.write(template_html)
