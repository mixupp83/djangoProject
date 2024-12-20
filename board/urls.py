from django.urls import path
from . import views

# Пространство имен приложения
app_name = 'board'

# URL-шаблоны для приложения
urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),  # Список объявлений
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),  # Детали объявления
    path('add/', views.add_advertisement, name='add_advertisement'),  # Добавление нового объявления
]