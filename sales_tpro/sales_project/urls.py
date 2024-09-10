from django.urls import path
from . import views  # Импортируем представления из текущего приложения

urlpatterns = [
    path('', views.home, name='home'),
    path('abc-xyz-analysis/', views.abc_xyz_analysis, name='abc_xyz_analysis'),
    path('export-forecast/', views.export_forecast, name='export_forecast'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('upload-sales/', views.upload_sales_file, name='upload_sales_file'),
    path('upload-stock/', views.upload_stock_file, name='upload_stock_file'),
    path('upload-supplier/', views.upload_supplier_file, name='upload_supplier_file'),
    path('upload-file/', views.upload_file_view, name='upload_file_view'),  # Путь для загрузки файлов

]