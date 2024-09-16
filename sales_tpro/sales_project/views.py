from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
import pandas as pd
import logging
from .forms import SalesFileUploadForm, SupplierFileUploadForm, UserRegistrationForm, StockFileUploadForm
from .models import SalesRecord, SupplierRecord, StockRecord
from .abc_xyz_analysis import load_sales_data, load_supplier_data, abc_xyz_classification, calculate_profitability
from django.conf import settings
import os
from .forecast_calculations import load_forecast_sales_data, load_stock_data, calculate_forecast
from django.contrib.auth.decorators import login_required


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

def custom_logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправляем на главную страницу после выхода


# Вход пользователя
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Страница выбора действий (Dashboard)
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')

# Загрузка файла продаж
def upload_sales_file(request):
    if request.method == 'POST':
        form = SalesFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            process_sales_file(request.FILES['file'])  # Обработка файла после загрузки
            messages.success(request, 'Файл продаж загружен и обработан!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка при загрузке файла продаж. Пожалуйста, попробуйте еще раз.')
    else:
        form = SalesFileUploadForm()
    return render(request, 'upload_sales_file.html', {'form': form})

# Загрузка файла поставщиков
def upload_supplier_file(request):
    if request.method == 'POST':
        form = SupplierFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            process_supplier_file(request.FILES['file'])  # Обработка файла после загрузки
            messages.success(request, 'Файл поставщиков загружен и обработан!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка при загрузке файла поставщиков. Пожалуйста, попробуйте еще раз.')
    else:
        form = SupplierFileUploadForm()
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
def abc_xyz_analysis_view(request, period):
    try:
        logger.info("Начало анализа ABC-XYZ")
        
        sales_file_path = os.path.join(settings.MEDIA_ROOT, 'sales_files', 'sales_file.csv')
        supplier_file_path = os.path.join(settings.MEDIA_ROOT, 'supplier_files', 'supplier_file.csv')
        
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
        
        sales_data = load_sales_data(sales_file_path)
        supplier_data = load_supplier_data(supplier_file_path)
        
        if sales_data is None or supplier_data is None:
            raise ValueError("Не удалось загрузить данные.")
        
        profitability_data = calculate_profitability(sales_data, supplier_data)
        analysis_results = abc_xyz_classification(profitability_data)
        
        context = {'period': period, 'analysis_results': analysis_results.to_dict(orient='records')}
        logger.info(f"Результаты анализа: {context['analysis_results']}")
        return render(request, 'abc_xyz_analysis.html', context)
    except Exception as e:
        logger.error(f"Ошибка при выполнении анализа ABC-XYZ: {e}")
        return render(request, 'error.html', {'message': f"Ошибка при выполнении анализа: {str(e)}"})

# Прогноз продаж
def sales_forecast_view(request, months):
    try:
        # Пути к файлам
        sales_file_path = os.path.join(settings.MEDIA_ROOT, 'sales_files', 'sales_file.csv')
        stock_file_path = os.path.join(settings.MEDIA_ROOT, 'stock_files', 'Stock.csv')

        # Загрузка данных
        sales_df = load_forecast_sales_data(sales_file_path)
        stock_df = load_stock_data(stock_file_path)

        # Отладочные сообщения
        print("Sales DataFrame head:\n", sales_df.head())
        print("Stock DataFrame head:\n", stock_df.head())

        # Убедитесь, что 'product_id' имеет одинаковый тип в обоих DataFrame
        sales_df['product_id'] = sales_df['product_id'].astype(str)
        stock_df['product_id'] = stock_df['product_id'].astype(str)

        # Рассчитайте прогноз
        forecast_df = calculate_forecast(sales_df, stock_df, months)

        # Убедитесь, что forecast_df содержит ожидаемые колонки
        required_columns = [f'Month_{month}' for month in range(1, months + 1)]
        missing_columns = [col for col in required_columns if col not in forecast_df.columns]
        if missing_columns:
            raise ValueError(f"Отсутствуют колонки в DataFrame прогноза: {', '.join(missing_columns)}")

        # Отладочные сообщения
        print("Forecast DataFrame head:\n", forecast_df.head())

        # Подготовка данных для шаблона
        context = {
            'forecast_results': forecast_df.to_dict(orient='records'),
        }

        # Отображение шаблона
        return render(request, 'sales_forecast.html', context)
    except Exception as e:
        # Логирование ошибки
        logger.error(f"Ошибка при прогнозировании продаж: {e}")
        return render(request, 'error.html', {'message': f'Ошибка при прогнозировании продаж: {str(e)}'})


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
                quantity=row['stock']  # Примечание: здесь исправлено 'quantity' на 'stock'
            )
        logger.info("Файл склада успешно обработан")
    except Exception as e:
        logger.error(f"Ошибка при обработке файла склада: {str(e)}")

# Страница заказа поставок
def supplier_order_view(request, months):
    try:
        # Вы можете добавить логику для обработки заказа поставок здесь.
        # Временный контекст для примера
        context = {'months': months}
        return render(request, 'supplier_order.html', context)
    except Exception as e:
        logger.error(f"Ошибка при обработке заказа поставок: {e}")
        return render(request, 'error.html', {'message': f'Ошибка при обработке заказа поставок: {str(e)}'})
