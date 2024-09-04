import pandas as pd
from .models import SalesRecord, Product, Supplier

def import_sales_data(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Iterate over the rows and save them to the SalesRecord model
    for index, row in df.iterrows():
        product, created = Product.objects.get_or_create(name=row['Product Name'])
        SalesRecord.objects.create(
            product=product,
            period=row['Period'],
            quantity=row['Quantity']
        )

def import_stock_data(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Iterate over the rows and update the stock in the Product model
    for index, row in df.iterrows():
        product, created = Product.objects.get_or_create(name=row['Product Name'])
        product.stock = row['Stock']
        product.save()

def import_supplier_data(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Iterate over the rows and save them to the Supplier model
    for index, row in df.iterrows():
        Supplier.objects.create(
            name=row['Supplier Name'],
            contact_info=row['Contact Info']
        )
        product, created = Product.objects.get_or_create(name=row['Product Name'])
        product.price = row['Price']
        product.save()