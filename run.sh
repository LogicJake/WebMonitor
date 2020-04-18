#!/bin/bash
python manage.py migrate
python manage.py initadmin --username $2 --password $3
python manage.py runserver 0.0.0.0:$1 --noreload
