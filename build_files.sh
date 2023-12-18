#!/bin/bash
pip install -r requirements.txt

python3.9 manage.py migrate
python3.9 manage.py createsuperuser --email=admin@a.com --username=admin --password=admin --noinput
