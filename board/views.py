from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
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
    advertisements_list = Advertisement.objects.all().order_by('-created_at')  # Сортируем по дате создания (новые сначала)
    paginator = Paginator(advertisements_list, 5)  # Ограничиваем количество объявлений на странице до 5

    page_number = request.GET.get('page')  # Получаем номер страницы из запроса
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы

    return render(request, 'board/advertisement_list.html', {'page_obj': page_obj})

# Представление для деталей объявления
def advertisement_detail(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})

# Представление для добавления нового объявления
@login_required
def add_advertisement(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)  # Добавлено request.FILES
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user  # Устанавливаем текущего пользователя как автора
            advertisement.save()
            return redirect('board:advertisement_list')  # Перенаправление на список объявлений
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})

# Представление для редактирования объявления
@login_required
def edit_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if advertisement.author != request.user:
        return redirect('board:advertisement_detail', pk=advertisement.pk)

    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)  # Добавлено request.FILES
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


# Представление для обработки лайка
@login_required
def like_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    advertisement.likes += 1
    advertisement.save()

    # Обновляем статистику пользователя
    profile = advertisement.author.profile
    profile.total_likes += 1
    profile.save()

    return JsonResponse({'likes': advertisement.likes})


# Представление для обработки дизлайка
@login_required
def dislike_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    advertisement.dislikes += 1
    advertisement.save()

    # Обновляем статистику пользователя
    profile = advertisement.author.profile
    profile.total_dislikes += 1
    profile.save()

    return JsonResponse({'dislikes': advertisement.dislikes})
