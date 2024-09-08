from django.apps import AppConfig


class SalesProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_project'

class SalesProjectConfig(AppConfig):
    name = 'sales_project'

    def ready(self):
        import sales_project.signals  # Импортируйте ваш файл сигналов