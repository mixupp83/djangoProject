from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),  # Список объявлений
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),  # Детали объявления
    path('advertisement/<int:pk>/edit/', views.edit_advertisement, name='edit_advertisement'),  # Редактирование объявления
    path('advertisement/<int:pk>/delete/', views.delete_advertisement, name='delete_advertisement'),  # Удаление объявления
    path('add/', views.add_advertisement, name='add_advertisement'),  # Добавление нового объявления
    path('advertisement/<int:pk>/like/', views.like_advertisement, name='like_advertisement'),  # Лайк объявления
    path('advertisement/<int:pk>/dislike/', views.dislike_advertisement, name='dislike_advertisement'),  # Дизлайк объявления
]