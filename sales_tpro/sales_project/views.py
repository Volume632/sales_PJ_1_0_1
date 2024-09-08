from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SalesFileForm, SupplierFileForm, ProductFileForm
from .models import SalesRecord, Product, Supplier
from .utils import import_sales_data, import_stock_data, import_supplier_data
import csv
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from .utils import predict_sales
import pandas as pd
from sales_project.predictor import predict_sales
from .models import SalesFile, SupplierFile
import logging
from django.core.exceptions import ValidationError
from sales_project.models import Product, SalesRecord

def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def upload_sales_file(request):
    if request.method == 'POST':
        form = SalesFileForm(request.POST, request.FILES)
        if form.is_valid():
            sales_file = form.save()
            import_sales_data(sales_file.file.path)
            messages.success(request, 'Sales data uploaded and processed successfully!')
            return redirect('home')
    else:
        form = SalesFileForm()
    return render(request, 'sales/upload_sales.html', {'form': form})

def upload_stock_file(request):
    if request.method == 'POST':
        form = ProductFileForm(request.POST, request.FILES)
        if form.is_valid():
            stock_file = request.FILES['file']
            import_stock_data(stock_file.temporary_file_path())
            messages.success(request, 'Stock data uploaded successfully!')
            return redirect('home')
    else:
        form = ProductFileForm()
    return render(request, 'sales/upload_stock.html', {'form': form})

def upload_supplier_file(request):
    if request.method == 'POST':
        form = SupplierFileForm(request.POST, request.FILES)
        if form.is_valid():
            supplier_file = form.save()
            import_supplier_data(supplier_file.file.path)
            messages.success(request, 'Supplier data uploaded successfully!')
            return redirect('home')
    else:
        form = SupplierFileForm()
    return render(request, 'sales/upload_supplier.html', {'form': form})


logger = logging.getLogger(__name__)

def abc_xyz_analysis(request):
    # Получаем все данные о продажах
    sales_records = SalesRecord.objects.select_related('product').all()

    # Преобразуем данные в DataFrame для анализа
    sales_data = []
    for record in sales_records:
        sales_data.append({
            'product_id': record.product.id,  # Используем 'product_id'
            'product_name': record.product.name,
            'price': record.product.price1 or record.product.price2,
            'period': record.period,
            'quantity': record.quantity
        })

    df = pd.DataFrame(sales_data)

    # Выводим структуру DataFrame для отладки
    print(df.head())
    print(df.columns)

    # Проверяем наличие всех необходимых столбцов
    required_columns = ['product_id', 'product_name', 'price', 'period', 'quantity']
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Неверная структура данных: отсутствует столбец '{column}'.")

    # Приведение типов
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df.dropna(subset=['quantity', 'price'], inplace=True)

    # ABC анализ: группировка по продукту и подсчёт общего объёма продаж
    abc_data = df.groupby('product_id').agg({'quantity': 'sum', 'price': 'mean'}).reset_index()

    # XYZ анализ: группировка по периоду
    xyz_data = df.groupby(['product_id', 'period']).agg({'quantity': 'sum'}).reset_index()

    # Передаем данные в шаблон
    context = {
        'abc_data': abc_data,
        'xyz_data': xyz_data
    }
    return render(request, 'abc_xyz_analysis.html', context)


def export_forecast(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="forecast.csv"'

    writer = csv.writer(response)
    writer.writerow(['Месяц', 'Прогноз'])

    # Пример данных для прогноза
    forecast_data = [
        ['Сентябрь', 100],
        ['Октябрь', 120],
        ['Ноябрь', 140],
]

    for row in forecast_data:
        writer.writerow(row)

    return response


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def forecast_sales_view(request):
    if request.method == 'POST':
        form = SalesFileForm(request.POST, request.FILES)
        if form.is_valid():
            sales_file = request.FILES['file']
            data = pd.read_excel(sales_file)
            forecast = predict_sales(data)
            # Передайте прогноз в шаблон или сохраните
    else:
        form = SalesFileForm()
    return render(request, 'sales/forecast_sales.html', {'form': form})


from django.core.exceptions import ValidationError
from sales_project.models import Product, SalesRecord

def process_sales_file(file_path):
    import pandas as pd
    
    df = pd.read_excel(file_path)

    # Проверка наличия всех product_id в базе данных
    existing_product_ids = set(Product.objects.values_list('id', flat=True))
    for product_id in df['product_id']:
        if product_id not in existing_product_ids:
            raise ValidationError(f"Product ID {product_id} does not exist in the database")

    # Сохранение данных
    for _, row in df.iterrows():
        SalesRecord.objects.create(
            period=row['period'],
            product_id=row['product_id'],
            quantity=row['quantity']
        )