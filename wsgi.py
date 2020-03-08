# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 19:53:12
# @Last Modified time: 2019-03-12 18:31:47
import os

from app import create_app

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)

env = os.getenv('FLASK_ENV') or 'production'
app = create_app(env)
