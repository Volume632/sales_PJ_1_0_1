from django.contrib import admin
from sales_project.models import SalesRecord, Product, Supplier, StockRecord, SalesFile, StockFile, SupplierFile

@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'get_period', 'created_at')  # Убедитесь, что 'created_at' существует
    list_filter = ('product', 'created_at')  # Фильтрация по продукту и дате создания
    search_fields = ('product__name',)  # Поиск по имени продукта
    date_hierarchy = 'created_at'  # Навигация по дате

    def get_period(self, obj):
        return obj.date.strftime("%B %Y")  # Период на основе даты
    get_period.short_description = 'Period'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price1', 'price2', 'created_at')
    search_fields = ('name',)  # Поиск по названию продукта
    list_filter = ('created_at',)  # Фильтрация по дате создания
    ordering = ('name',)  # Сортировка по имени

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'created_at')
    search_fields = ('name', 'contact_info')  # Поиск по имени и контактной информации
    list_filter = ('created_at',)  # Фильтрация по дате создания

@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'created_at')
    search_fields = ('product__name',)  # Поиск по имени продукта
    list_filter = ('product', 'created_at')  # Фильтрация по продукту и дате создания

@admin.register(SalesFile)
class SalesFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    list_filter = ('uploaded_at',)  # Фильтрация по дате загрузки
    search_fields = ('file',)  # Поиск по имени файла

@admin.register(StockFile)
class StockFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    list_filter = ('uploaded_at',)  # Фильтрация по дате загрузки
    search_fields = ('file',)  # Поиск по имени файла

@admin.register(SupplierFile)
class SupplierFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    list_filter = ('uploaded_at',)  # Фильтрация по дате загрузки
    search_fields = ('file',)  # Поиск по имени файла
