from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertisement
from .forms import AdvertisementForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate

# Представление для выхода
def logout_view(request):
    logout(request)
    return redirect('home')

# Представление для регистрации
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'board/signup.html', {'form': form})

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

# Представление для добавления объявления
@login_required
def add_advertisement(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})


@login_required
def edit_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)

    if advertisement.author != request.user:
        return redirect('board:advertisement_list')

    if request.method == "POST":
        form = AdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            form.save()
            return redirect('board:advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm(instance=advertisement)

    return render(request, 'board/edit_advertisement.html', {'form': form, 'advertisement': advertisement})