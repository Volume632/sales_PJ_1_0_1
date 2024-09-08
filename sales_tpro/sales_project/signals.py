from django.db.models.signals import post_save
from django.dispatch import receiver
from sales_project.models import SalesFile
from sales_project.utils import process_sales_file

@receiver(post_save, sender=SalesFile)
def handle_sales_file(sender, instance, **kwargs):
    if instance.file:  # Убедитесь, что файл загружен
        process_sales_file(instance.file.path)