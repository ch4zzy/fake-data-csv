#!/bin/bash
pip install -r requirements.txt

python3.9 manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@a.com', 'admin')" | python3.9 manage.py shell

