import pandas as pd
from .models import SalesRecord, Product, Supplier
from sales_project.predictor import predict_sales



# Функция для импорта данных о продажах
def import_sales_data(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        try:
            product = Product.objects.get(id=row['id'])
            SalesRecord.objects.update_or_create(
                period=row['period'],
                product=product,
                defaults={'quantity': row['sales']}
            )
        except Product.DoesNotExist:
            print(f"Product with ID {row['id']} not found in database.")

def import_stock_data(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Iterate over the rows and update the stock in the Product model
    for index, row in df.iterrows():
        product, created = Product.objects.get_or_create(name=row['Product Name'])
        product.stock = row['Stock']
        product.save()

# Функция для импорта данных о прайсах
def import_supplier_data(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Product.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row['product_name'],
                'price1': row['price1'],
                'price2': row['price2']
            }
        )

def process_sales_file(file_path):
    df = pd.read_excel(file_path)

    # Убедитесь, что данные соответствуют ожидаемой структуре
    if 'product_id' not in df.columns:
        raise ValueError("Неверная структура данных: отсутствует столбец 'product_id'.")

    # Обработка данных и сохранение в базу данных
    for _, row in df.iterrows():
        SalesRecord.objects.create(
            period=row['period'],
            product_id=row['product_id'],
            quantity=row['quantity']
        )