python manage.py migrate --no-input;

python manage.py createsuperuser --noinput;

gunicorn --workers 2 --bind 0.0.0.0:8000 sales_project.wsgi:application;