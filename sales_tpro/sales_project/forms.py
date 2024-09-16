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

# Форма для регистрации с email
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email

# Общая форма для загрузки файлов CSV
class FileUploadForm(forms.ModelForm):
    file = forms.FileField(label='Выберите файл CSV')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.csv'):
            raise forms.ValidationError("Загружаемый файл должен быть формата .csv")
        return file

# Форма для загрузки файла с данными о продажах
class SalesFileUploadForm(FileUploadForm):
    class Meta:
        model = SalesFile
        fields = ['file']
        labels = {'file': 'Загрузите файл с данными о продажах'}

# Форма для загрузки файла с данными от поставщиков
class SupplierFileUploadForm(FileUploadForm):
    class Meta:
        model = SupplierFile
        fields = ['file']
        labels = {'file': 'Загрузите файл с данными от поставщиков'}

# Форма для загрузки файла данных о запасах
class StockFileUploadForm(FileUploadForm):
    class Meta:
        model = StockFile
        fields = ['file']
        labels = {'file': 'Загрузите файл с данными о запасах'}

# Форма для аутентификации пользователя
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'
