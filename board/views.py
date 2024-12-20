from django.shortcuts import render, redirect
from board.models import Advertisement
from board.forms import AdvertisementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Представление для выхода из системы
def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправление на домашнюю страницу

# Представление для регистрации пользователя
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/board')  # Перенаправление на страницу объявлений
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Представление для домашней страницы
def home(request):
    return render(request, 'home.html')

# Представление для списка объявлений
def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})

# Представление для деталей объявления
def advertisement_detail(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})

# Представление для добавления нового объявления (только для авторизованных пользователей)
@login_required
def add_advertisement(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user  # Устанавливаем текущего пользователя как автора
            advertisement.save()
            return redirect('board:advertisement_list')  # Перенаправление на список объявлений
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})