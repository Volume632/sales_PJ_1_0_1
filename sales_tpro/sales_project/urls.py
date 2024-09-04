from django.contrib import admin
from django.urls import path
from sales import views  # Импортируем views из приложения sales
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('abc-xyz-analysis/', views.abc_xyz_analysis, name='abc_xyz_analysis'),
    path('export-forecast/', views.export_forecast, name='export_forecast'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),  # Убедитесь, что register_view определен
    path('upload-sales/', views.upload_sales_file, name='upload_sales_file'),
    path('upload-stock/', views.upload_stock_file, name='upload_stock_file'),
    path('upload-supplier/', views.upload_supplier_file, name='upload_supplier_file'),
]