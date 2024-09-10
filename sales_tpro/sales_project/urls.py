from django.urls import path
from . import views 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('abc-xyz-analysis/<str:period>/', views.abc_xyz_analysis, name='abc_xyz_analysis'),
    path('sales-forecast/<int:months>/', views.sales_forecast, name='sales_forecast'),
    path('supplier-order/<int:months>/', views.supplier_order, name='supplier_order'),
    path('upload-sales/', views.upload_sales_file, name='upload_sales_file'),
    path('upload-stock/', views.upload_stock_file, name='upload_stock_file'),
    path('upload-supplier/', views.upload_supplier_file, name='upload_supplier_file'),
    path('logout/', LogoutView.as_view(), name='logout'),
]