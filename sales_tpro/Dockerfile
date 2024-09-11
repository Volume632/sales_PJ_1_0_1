# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт запуска и делаем его исполняемым
COPY run.sh /run.sh

RUN chmod +x /run.sh

# Копируем весь проект в рабочую директорию
COPY . /app

# Устанавливаем переменную окружения для Django
ENV DJANGO_SETTINGS_MODULE=sales_tpro.settings

# Выполняем миграции и запускаем сервер с gunicorn
CMD ["/run.sh"]
