from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertisement
from .forms import AdvertisementForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate


# Представление для выхода из системы
def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправление на домашнюю страницу


# Представление для регистрации пользователя
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
    advertisement = get_object_or_404(Advertisement, pk=pk)
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


# Представление для редактирования объявления (только для авторизованных пользователей)
@login_required
def edit_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    # Проверка, что текущий пользователь является автором объявления
    if advertisement.author != request.user:
        return redirect('board:advertisement_detail', pk=advertisement.pk)

    if request.method == "POST":
        form = AdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            form.save()
            return redirect('board:advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'board/edit_advertisement.html', {'form': form, 'advertisement': advertisement})


# Представление для удаления объявления
@login_required
def delete_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)

    # Проверка, что текущий пользователь является автором объявления
    if advertisement.author != request.user:
        return redirect('board:advertisement_detail', pk=advertisement.pk)

    if request.method == "POST":
        # Удаление объявления после подтверждения
        advertisement.delete()
        return redirect('board:advertisement_list')  # Перенаправление на список объявлений

    return render(request, 'board/delete_advertisement.html', {'advertisement': advertisement})
