# Используем базовый образ Python
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/sales_tpro

ENV DJANGO_SETTINGS_MODULE=sales_tpro.settings

# Выполняем миграции и запускаем сервер с gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py createsuperuser --noinput && gunicorn sales_tpro.wsgi:application --bind 0.0.0.0:8000"]