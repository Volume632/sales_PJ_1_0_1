from django.db import models
from datetime import date
import uuid
from django.core.exceptions import ValidationError  # Для валидации файлов
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings

# Валидация типа файла (например, только CSV)
def validate_file_extension(value):
    if not value.name.endswith('.csv'):
        raise ValidationError("Только файлы с расширением .csv поддерживаются.")

# Модель для продуктов
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    price1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Цена может быть null
    price2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Альтернативная цена
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Время последнего обновления

    def __str__(self):
        return self.name

# Модель для записей о продажах
class SalesRecord(models.Model):
    sale_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Уникальный идентификатор продажи (UUID)
    date = models.DateField(default=date.today)  # Значение по умолчанию — текущая дата
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Связь с продуктом
    quantity = models.IntegerField()  # Количество проданных товаров
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Общая цена (автовычисление)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Время последнего обновления

    @property
    def period(self):
        return self.date.strftime("%B %Y")  # Преобразование даты в формат "Месяц Год"

    def save(self, *args, **kwargs):
        # Автоматическое вычисление общей цены на основе цены продукта и количества
        self.total_price = (self.product.price1 or self.product.price2) * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale {self.sale_id} - {self.product.name}"

# Модель для остатка товаров
class StockRecord(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Связь с продуктом
    quantity = models.IntegerField()  # Количество на складе
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Время последнего обновления

    def __str__(self):
        return f"{self.product.name} - Stock: {self.quantity}"

# Модель для поставщиков
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)  # Уникальное имя поставщика
    contact_info = models.TextField()  # Контактная информация поставщика
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Время последнего обновления

    def __str__(self):
        return self.name

# Модель для загрузки файлов остатков
class StockFile(models.Model):
    file = models.FileField(upload_to='stock_files/', validators=[validate_file_extension])  # Поле для загрузки файла остатков с валидацией
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Время загрузки файла

    def __str__(self):
        return f"Stock File: {os.path.basename(self.file.name)} (Uploaded at: {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')})"

    def delete(self, *args, **kwargs):
        # Удаление файла из системы при удалении записи из БД
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

# Модель для загрузки файлов продаж
class SalesFile(models.Model):
    file = models.FileField(upload_to='sales_files/', validators=[validate_file_extension])  # Поле для загрузки файла с валидацией
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Время загрузки файла

    def __str__(self):
        return f"Sales File: {os.path.basename(self.file.name)} (Uploaded at: {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')})"

    def delete(self, *args, **kwargs):
        # Удаление файла из системы при удалении записи из БД
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

# Модель для загрузки файлов поставщиков
class SupplierFile(models.Model):
    file = models.FileField(upload_to='supplier_files/', validators=[validate_file_extension])  # Поле для загрузки файла поставщиков с валидацией
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Время загрузки файла

    def __str__(self):
        return f"Supplier File: {os.path.basename(self.file.name)} (Uploaded at: {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')})"

    def delete(self, *args, **kwargs):
        # Удаление файла из системы при удалении записи из БД
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

# Сигнал для удаления файлов после удаления объектов моделей
@receiver(post_delete, sender=StockFile)
@receiver(post_delete, sender=SalesFile)
@receiver(post_delete, sender=SupplierFile)
def delete_file_on_delete(sender, instance, **kwargs):
    """Удаление файла после удаления объекта модели"""
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
