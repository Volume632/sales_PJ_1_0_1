from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Админ-панель
    path('', include('sales_project.urls')),  # Основное приложение sales_project
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# В случае продакшена медиафайлы лучше обслуживать через веб-сервер (например, Nginx)

