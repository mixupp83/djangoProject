from django import forms
from .models import Advertisement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Форма для создания объявления
class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'content']  # Поля формы: заголовок и содержимое объявления
        # Поле 'author' не включено, так как оно автоматически устанавливается текущим пользователем


# Форма для регистрации пользователя
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Поля формы: имя пользователя и пароль
