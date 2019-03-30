# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 19:53:12
# @Last Modified time: 2019-03-12 18:31:47
import os

from app import create_app
from md2html import Markdown2Html

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)

index_html = os.path.join(
    os.path.dirname(__file__), 'app', 'templates', 'admin', 'index.html')
m2h = Markdown2Html()
m2h.convert('README.md', index_html)

app = create_app(os.getenv("FLASK_ENV"))
