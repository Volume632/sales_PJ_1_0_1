from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
import pandas as pd
import logging
from .forms import SalesFileForm, SupplierFileForm, UserRegistrationForm, StockFileUploadForm
from .models import SalesRecord, SupplierRecord, StockRecord
from .abc_xyz_analysis import load_sales_data, load_supplier_data, abc_xyz_classification, calculate_profitability
from django.conf import settings
import os

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
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
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
            process_sales_file(request.FILES['file'])  # Обработка файла после загрузки
            messages.success(request, 'Файл продаж загружен и обработан!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка при загрузке файла продаж. Пожалуйста, попробуйте еще раз.')
    else:
        form = SalesFileForm()
    return render(request, 'upload_sales_file.html', {'form': form})

# Загрузка файла поставщиков
def upload_supplier_file(request):
    if request.method == 'POST':
        form = SupplierFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            process_supplier_file(request.FILES['file'])  # Обработка файла после загрузки
            messages.success(request, 'Файл поставщиков загружен и обработан!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка при загрузке файла поставщиков. Пожалуйста, попробуйте еще раз.')
    else:
        form = SupplierFileForm()
    return render(request, 'upload_supplier_file.html', {'form': form})

# Обработка файла продаж
def process_sales_file(file):
    try:
        df = pd.read_csv(file, delimiter=';')
        # Суммирование quantity для повторяющихся product_id
        df = df.groupby('product_id', as_index=False).agg({'quantity': 'sum', 'period': 'first'})
        
        for index, row in df.iterrows():
            SalesRecord.objects.create(
                product_id=row['product_id'],
                quantity=row['quantity'],
                date=pd.to_datetime(row['period']).date()
            )
        logger.info("Файл продаж успешно обработан")
    except Exception as e:
        logger.error(f"Ошибка при обработке файла продаж: {str(e)}")

# Обработка файла поставщиков
def process_supplier_file(file):
    try:
        df = pd.read_csv(file, delimiter=';')
        for index, row in df.iterrows():
            SupplierRecord.objects.update_or_create(
                product_id=row['product_id'],
                defaults={
                    'name': row['Name'],
                    'price2': row['price2']
                }
            )
        logger.info("Файл поставщиков успешно обработан")
    except Exception as e:
        logger.error(f"Ошибка при обработке файла поставщиков: {str(e)}")

# Отображение страницы анализа ABC/XYZ
import os

def abc_xyz_analysis_view(request, period):
    try:
        logger.info("Начало анализа ABC-XYZ")
        
        # Замените этот путь на путь к файлу, который вы используете
        sales_file_path = r'D:\Python\sales_PJ_1_0_1\sales_tpro\media\sales_files\sales_file.csv'
        supplier_file_path = r'D:\Python\sales_PJ_1_0_1\sales_tpro\media\supplier_files\supplier_file.csv'
        
        # Проверка наличия файлов
        def check_file_exists(file_path):
            if os.path.isfile(file_path):
                return True
            else:
                logger.error(f"Файл не найден: {file_path}")
                return False
        
        if not check_file_exists(sales_file_path):
            raise FileNotFoundError(f"Файл продаж не найден: {sales_file_path}")
        if not check_file_exists(supplier_file_path):
            raise FileNotFoundError(f"Файл поставщиков не найден: {supplier_file_path}")
        
        # Загрузка данных
        sales_data = load_sales_data(sales_file_path)
        supplier_data = load_supplier_data(supplier_file_path)
        
        # Проверка загруженных данных
        if sales_data is None or supplier_data is None:
            raise ValueError("Не удалось загрузить данные.")
        
        # Рассчет доходности
        profitability_data = calculate_profitability(sales_data, supplier_data)
        
        # ABC-XYZ классификация
        analysis_results = abc_xyz_classification(profitability_data)
        
        # Передача результатов в шаблон
        context = {'period': period, 'analysis_results': analysis_results.to_dict(orient='records')}
        logger.info(f"Результаты анализа: {context['analysis_results']}")
        return render(request, 'abc_xyz_analysis.html', context)
    except Exception as e:
        logger.error(f"Ошибка при выполнении анализа ABC-XYZ: {e}")
        return render(request, 'error.html', {'message': f"Ошибка при выполнении анализа: {str(e)}"})

# Прогноз продаж
def sales_forecast(request, months):
    try:
        # Пример простого прогноза продаж
        forecast_data = [{'month': f'Month {i + 1}', 'forecast': 100 * (i + 1)} for i in range(months)]
        
        # Передача данных в шаблон
        context = {'forecast_data': forecast_data, 'months': months}
        return render(request, 'forecast.html', context)
    except Exception as e:
        return render(request, 'error.html', {'message': f'Ошибка при прогнозе продаж: {e}'})

# Заказ у поставщика
def supplier_order(request, months):
    try:
        # Пример заказа поставщику
        order_data = [{'month': f'Month {i + 1}', 'order': 50 * (i + 1)} for i in range(months)]
        
        # Передача данных в шаблон
        context = {'order_data': order_data, 'months': months}
        return render(request, 'supplier_order.html', context)
    except Exception as e:
        return render(request, 'error.html', {'message': f'Ошибка при создании заказа: {e}'})

# Загрузка файла склада
def upload_stock_file(request):
    if request.method == 'POST':
        form = StockFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            process_stock_file(request.FILES['file'])  # Обработка файла после загрузки
            messages.success(request, 'Файл склада загружен и обработан!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка при загрузке файла склада. Пожалуйста, попробуйте еще раз.')
    else:
        form = StockFileUploadForm()
    return render(request, 'upload_stock_file.html', {'form': form})

# Обработка файла склада
def process_stock_file(file):
    try:
        df = pd.read_csv(file, delimiter=';')
        for index, row in df.iterrows():
            StockRecord.objects.create(
                product_id=row['product_id'],
                quantity=row['quantity'],
                date=pd.to_datetime(row['period']).date()
            )
        logger.info("Файл склада успешно обработан")
    except Exception as e:
        logger.error(f"Ошибка при обработке файла склада: {str(e)}")
