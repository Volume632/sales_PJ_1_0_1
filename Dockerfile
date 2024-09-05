# Используем базовый образ Python
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/sales_tpro

EXPOSE 8000

CMD ["/bin/sh", "run.sh"]