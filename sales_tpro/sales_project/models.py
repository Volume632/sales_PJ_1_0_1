from django.db import models

# Модель для продуктов
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    price1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Модель для записей о продажах
class SalesRecord(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.period}"

# Модель для остатка товаров
class StockRecord(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Stock: {self.quantity}"

# Модель для поставщиков
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    contact_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Модель для загрузки файлов продаж
class SalesFile(models.Model):
    file = models.FileField(upload_to='sales_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sales File: {self.file.name}"

# Модель для загрузки файлов остатков
class StockFile(models.Model):
    file = models.FileField(upload_to='stock_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock File: {self.file.name}"

# Модель для загрузки файлов прайсов поставщика
class SupplierFile(models.Model):
    file = models.FileField(upload_to='supplier_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Supplier File: {self.file.name}"