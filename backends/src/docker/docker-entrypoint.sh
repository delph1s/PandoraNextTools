#!/usr/bin/env bash

set -e

#python3 manage.py makemigrations&&
#python3 manage.py migrate&&
python3 manage.py runserver 0.0.0.0:8888
#uwsgi --ini /var/www/html/myproject/uwsgi.ini&&
#tail -f /dev/null

exec "$@"
