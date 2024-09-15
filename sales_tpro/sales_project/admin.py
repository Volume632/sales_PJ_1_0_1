from django.contrib import admin
from sales_project.models import SalesRecord, Product, SalesFile, StockFile, SupplierFile, SupplierRecord, StockRecord


@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'get_period', 'created_at')
    list_filter = ('product', 'created_at')
    search_fields = ('product__name',)
    date_hierarchy = 'created_at'

    def get_period(self, obj):
        return obj.date.strftime("%B %Y")
    get_period.short_description = 'Period'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price1', 'price2', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('name',)


@admin.register(SupplierRecord)  # Здесь используем SupplierRecord
class SupplierRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_id', 'price2', 'created_at')
    search_fields = ('name', 'product_id')
    list_filter = ('created_at',)


@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'created_at')
    search_fields = ('product__name',)
    list_filter = ('product', 'created_at')


@admin.register(SalesFile)
class SalesFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('file',)


@admin.register(StockFile)
class StockFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('file',)


@admin.register(SupplierFile)
class SupplierFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('file',)
