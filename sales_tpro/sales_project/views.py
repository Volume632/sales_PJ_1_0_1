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

def abc_xyz_analysis(request):
    # Здесь должен быть код, выполняющий ABC-XYZ анализ.
    # Например, можно передать данные в шаблон для отображения
    context = {
        'analysis_results': [],  # Добавьте сюда результаты анализа
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