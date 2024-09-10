from django.db.models.signals import post_save
from django.dispatch import receiver
from sales_project.models import SalesFile
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

@receiver(post_save, sender=SalesFile)
def handle_sales_file(sender, instance, created, **kwargs):
    """
    Сигнал, срабатывающий после сохранения SalesFile.
    """
    if created and instance.file:  # Убедитесь, что файл загружен и это новая запись
        try:
            # Здесь можно добавить дополнительную логику для работы с файлом
            logger.info(f"Файл {instance.file.name} успешно загружен и сохранен по пути {instance.file.path}.")
        except Exception as e:
            logger.error(f"Ошибка при обработке файла {instance.file.path}: {e}")
