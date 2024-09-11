from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import SalesFile, SupplierFile, StockFile

# Форма для регистрации нового пользователя
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля'
        }
        help_texts = {
            'username': 'Введите уникальное имя пользователя.',
        }

# Общая форма для загрузки файлов CSV
class FileUploadForm(forms.Form):
    file = forms.FileField(label='Выберите файл CSV')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.csv'):
            raise forms.ValidationError("Загружаемый файл должен быть формата .csv")
        return file

# Форма для загрузки файла с данными о продажах
class SalesFileForm(forms.ModelForm):
    class Meta:
        model = SalesFile
        fields = ['file']  # Только поле для файла

# Форма для загрузки файла с данными от поставщиков
class SupplierFileForm(FileUploadForm):
    class Meta:
        model = SupplierFile
        fields = ['file']
        labels = {'file': 'Загрузите файл с данными от поставщиков'}

# Форма для аутентификации пользователя
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'

# Форма для регистрации с email
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Форма для загрузки файла данных о запасах
class StockFileUploadForm(forms.ModelForm):
    class Meta:
        model = StockFile
        fields = ['file']
