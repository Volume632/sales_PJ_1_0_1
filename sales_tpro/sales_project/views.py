from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
import csv
import pandas as pd
import logging
from django.db import transaction
from .forms import SalesFileForm, SupplierFileForm, CustomUserCreationForm, FileUploadForm
from .models import SalesFile, StockFile, SupplierFile
from .forms import UserRegistrationForm




logger = logging.getLogger(__name__)

# Главная страница
def home(request):
    return render(request, 'home.html')

# Логаут пользователя
def logout_view(request):
    logout(request)
    return redirect('home')

# Регистрация пользователя
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Вход пользователя
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

# Страница выбора действий
def dashboard(request):
    return render(request, 'dashboard.html')

# Загрузка файла продаж
def upload_sales_file(request):
    if request.method == 'POST':
        form = SalesFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sales file uploaded successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Error uploading sales file. Please try again.')
    else:
        form = SalesFileForm()
    return render(request, 'upload_sales_file.html', {'form': form})

# Загрузка файла поставщиков
def upload_supplier_file(request):
    if request.method == 'POST':
        form = SupplierFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier file uploaded successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Error uploading supplier file. Please try again.')
    else:
        form = SupplierFileForm()
    return render(request, 'sales/upload_supplier_file.html', {'form': form})

# Экспорт прогноза в CSV
def export_forecast(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="forecast.csv"'

    writer = csv.writer(response)
    writer.writerow(['Month', 'Forecast'])
    forecast_data = [['September', 100], ['October', 120], ['November', 140]]

    for row in forecast_data:
        writer.writerow(row)

    return response

# Отображение страницы анализа ABC/XYZ
def abc_xyz_analysis(request, period):
    abc_data = [{'product_id': 1, 'quantity': 100}]
    xyz_data = [{'product_id': 1, 'period': '2024-09', 'quantity': 50}]
    
    context = {'abc_data': abc_data, 'xyz_data': xyz_data, 'period': period}
    return render(request, 'abc_xyz_analysis.html', context)

# Загрузка файла и обработка без сохранения в базу данных
def upload_file_view(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = process_file(uploaded_file)
                    if df is not None:
                        return render(request, 'success.html', {'data': df.to_html()})
                    else:
                        return render(request, 'error.html', {'message': 'Error processing file'})
                else:
                    return render(request, 'error.html', {'message': 'Only CSV files are supported'})
            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                return render(request, 'error.html', {'message': f'Error processing file: {e}'})
        else:
            return render(request, 'error.html', {'message': 'No file uploaded'})
    return render(request, 'upload.html')

# Обработка файла (пример без сохранения в БД)
def process_file(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, delimiter=';')
        required_columns = {'quantity', 'product_id', 'period'}
        current_columns = set(df.columns.str.strip().str.lower())
        missing_columns = required_columns - current_columns
        if missing_columns:
            raise Exception(f"Missing required columns: {missing_columns}")
        return df
    except Exception as e:
        raise Exception(f'Error reading CSV file: {e}')

@transaction.atomic
def upload_stock_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                stock_file = request.FILES['file']
                if stock_file.name.endswith('.csv'):
                    # Обработка файла
                    StockFile.objects.create(file=stock_file)
                    messages.success(request, 'Файл с данными о складе успешно загружен!')
                    return redirect('home')
                else:
                    messages.error(request, 'Пожалуйста, загрузите файл в формате CSV.')
            except Exception as e:
                messages.error(request, f"Ошибка при загрузке файла: {str(e)}")
        else:
            messages.error(request, 'Неверная отправка формы.')
    else:
        form = FileUploadForm()
    return render(request, 'upload_stock.html', {'form': form})



def process_stock_file(stock_file):
    # Логика обработки файла stock_file
    pass

def sales_forecast(request, months):
    forecast_data = [{'month': months, 'forecast': 100 * int(months)}]
    context = {'forecast_data': forecast_data, 'months': months}
    return render(request, 'forecast.html', context)

def supplier_order(request, months):
    order_data = [{'month': months, 'order': 50 * int(months)}]
    context = {'order_data': order_data, 'months': months}
    return render(request, 'supplier_order.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}. Теперь вы можете войти.')
            login(request, user)  # Можно сразу логинить после регистрации
            return redirect('dashboard')  # Перенаправление на кабинет пользователя
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
