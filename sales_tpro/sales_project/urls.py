from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    
    # Регистрация пользователя
    path('register/', views.register_view, name='register'),
    
    # Панель управления (dashboard)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Анализ ABC/XYZ с параметром период
    path('abc-xyz-analysis/<str:period>/', views.abc_xyz_analysis_view, name='abc_xyz_analysis'),
    
    # Прогноз продаж
    path('sales-forecast/<int:months>/', views.sales_forecast_view, name='sales_forecast'),

    
    # Заказ у поставщика
    path('supplier-order/<int:months>/', views.supplier_order_view, name='supplier_order'),

    
    # Загрузка файла продаж
    path('upload-sales/', views.upload_sales_file, name='upload_sales_file'),
    
    # Загрузка файла запасов
    path('upload-stock/', views.upload_stock_file, name='upload_stock_file'),
    
    # Загрузка файла поставщиков
    path('upload-supplier/', views.upload_supplier_file, name='upload_supplier_file'),
    
    # Выход пользователя
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Вход пользователя
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
]

# Подключение статических файлов для разработки
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
