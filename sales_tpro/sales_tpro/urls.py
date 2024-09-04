from django.contrib import admin
from django.urls import path
from sales_project import views  # Import views from the sales app
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('abc-xyz-analysis/', views.abc_xyz_analysis, name='abc_xyz_analysis'),
    path('export-forecast/', views.export_forecast, name='export_forecast'),
    path('login/', views.login_view, name='login'),  # Используем пользовательский login_view
    path('logout/', views.logout_view, name='logout'),  # Используем пользовательский logout_view
    path('register/', views.register_view, name='register'),  # Убедитесь, что register_view определен в views.py
    path('upload-sales/', views.upload_sales_file, name='upload_sales_file'),
    path('upload-stock/', views.upload_stock_file, name='upload_stock_file'),
    path('upload-supplier/', views.upload_supplier_file, name='upload_supplier_file'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)