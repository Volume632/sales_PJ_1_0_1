# Sales and Stock Management System

Этот проект представляет собой систему управления продажами и запасами, которая включает в себя анализ ABC-XYZ, прогнозирование продаж и расчет заказов у поставщиков.

## Основные страницы:
1. **Главная страница** — начальная точка, с которой пользователь начинает работу.
2. **Страница регистрации** — регистрация новых пользователей.
3. **Дашборд** — выбор действий: загрузка файлов продаж или запасов, ABC-XYZ анализ и прогнозирование.
4. **Анализ ABC-XYZ** — выбор периода для анализа (полный период, 2024, 2023, 2022, 2021).
5. **Прогноз продаж** — прогнозирование продаж на 1, 2, 3 и 6 месяцев.
6. **Заказ поставщикам** — расчет заказов для поставщиков на 1, 2, 3 и 6 месяцев.

## Установка

1. **Клонирование репозитория:**
   ```bash
   git clone <ссылка на репозиторий>
   cd <название папки проекта>

2. Создание виртуального окружения:
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

3. Установка зависимостей:
pip install -r requirements.txt

4. Применение миграций базы данных:
python manage.py migrate

5. Запуск сервера:
python manage.py runserver

Как использовать
Перейдите на http://localhost:8000 для доступа к главной странице.
Зарегистрируйте нового пользователя.
После авторизации используйте дашборд для загрузки файлов CSV с данными по продажам и запасам, а также для анализа и прогнозирования.
Структура проекта
sales_project/: Основная директория проекта.
sales_app/: Приложение для загрузки файлов и анализа данных.
templates/: HTML-шаблоны для всех страниц.
static/: Статические файлы (CSS, JS).
media/: Загрузки CSV файлов.
styles.css: Основные стили проекта.
Зависимости
Python 3.x
Django 4.x
Pandas для анализа данных

Автор проекта: Захаров Г.О.