import pandas as pd
from .models import SalesRecord, Product, Supplier
from sales_project.predictor import predict_sales
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

# Функция для чтения Excel файлов
def read_excel_file(file):
    try:
        df = pd.read_excel(file, engine='openpyxl')
        return df
    except Exception as e:
        logger.error(f"Ошибка при чтении файла Excel: {str(e)}")
        raise

# Функция для импорта данных о продажах
def import_sales_data(file):
    try:
        df = read_excel_file(file)  # Чтение файла через отдельную функцию

        # Проверка структуры данных
        required_columns = ['id', 'period', 'sales']
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"Неверная структура данных: отсутствует столбец '{column}'.")

        # Открытие транзакции
        with transaction.atomic():
            for _, row in df.iterrows():
                try:
                    product = Product.objects.get(id=row['id'])
                    SalesRecord.objects.update_or_create(
                        period=row['period'],
                        product=product,
                        defaults={'quantity': row['sales']}
                    )
                except Product.DoesNotExist:
                    # Логирование ошибки и выход из транзакции
                    logger.error(f"Товар с ID {row['id']} не найден.")
                    raise Exception(f"Товар с ID {row['id']} не найден.")
                except Exception as e:
                    logger.error(f"Ошибка при обработке строки: {str(e)}")
                    raise  # Прерываем транзакцию при любой другой ошибке
    except Exception as e:
        # Общая обработка ошибок
        logger.error(f"Ошибка при импорте данных о продажах: {str(e)}")
        raise  # Прерывание, чтобы не продолжать работу с нарушенной транзакцией

# Функция для импорта данных о стоках
def import_stock_data(file):
    try:
        df = read_excel_file(file)

        # Проверка структуры данных
        required_columns = ['Product Name', 'Stock']
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"Неверная структура данных: отсутствует столбец '{column}'.")

        # Обработка данных
        with transaction.atomic():
            for _, row in df.iterrows():
                product, created = Product.objects.get_or_create(name=row['Product Name'])
                product.stock = row['Stock']
                product.save()
    except Exception as e:
        logger.error(f"Ошибка при импорте данных о стоках: {str(e)}")
        raise

# Функция для импорта данных о поставщиках
def import_supplier_data(file):
    try:
        df = read_excel_file(file)

        # Проверка структуры данных
        required_columns = ['id', 'product_name', 'price1', 'price2']
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"Неверная структура данных: отсутствует столбец '{column}'.")

        # Обработка данных
        with transaction.atomic():
            for _, row in df.iterrows():
                Product.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['product_name'],
                        'price1': row['price1'],
                        'price2': row['price2']
                    }
                )
    except Exception as e:
        logger.error(f"Ошибка при импорте данных о поставщиках: {str(e)}")
        raise

# Функция для обработки файла продаж
def process_sales_file(file):
    try:
        df = read_excel_file(file)

        # Проверка структуры данных
        if 'product_id' not in df.columns:
            raise ValueError("Неверная структура данных: отсутствует столбец 'product_id'.")

        # Обработка данных
        with transaction.atomic():
            for _, row in df.iterrows():
                SalesRecord.objects.create(
                    period=row['period'],
                    product_id=row['product_id'],
                    quantity=row['quantity']
                )
    except Exception as e:
        logger.error(f"Ошибка при обработке файла продаж: {str(e)}")
        raise

# Функция для обработки любого Excel файла (общая)
def process_file(file):
    try:
        df = read_excel_file(file)
        return df
    except Exception as e:
        logger.error(f"Ошибка при обработке файла: {str(e)}")
        raise
