from django.core.exceptions import ValidationError

# Валидация расширений файлов
def validate_file_extension(value):
    valid_extensions = ['.csv']
    if not any(value.name.endswith(ext) for ext in valid_extensions):
        raise ValidationError('Неправильный формат файла. Разрешены только файлы CSV.')