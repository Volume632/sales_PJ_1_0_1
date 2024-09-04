from django.contrib import admin
from sales_project.models import SalesRecord, Product, Supplier, StockRecord, SalesFile, StockFile, SupplierFile

@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'period', 'created_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price1', 'price2', 'created_at')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'created_at')

@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'created_at')

@admin.register(SalesFile)
class SalesFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')

@admin.register(StockFile)
class StockFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')

@admin.register(SupplierFile)
class SupplierFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')