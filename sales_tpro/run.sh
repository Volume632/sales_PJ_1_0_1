#!/bin/bash
python manage.py migrate
python manage.py createsuperuser --noinput
gunicorn sales_tpro.wsgi:application --bind 0.0.0.0:8000