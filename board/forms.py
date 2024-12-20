from django import forms
from .models import Advertisement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Форма для создания объявления
class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        # Поля, которые будут отображаться в форме
        fields = ['title', 'content', 'author']

# Форма для регистрации пользователя
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        # Поля, которые будут отображаться в форме регистрации
        fields = ('username', 'password1', 'password2',)