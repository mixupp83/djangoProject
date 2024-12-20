from django.db import models
from django.contrib.auth.models import User

# Модель для объявления
class Advertisement(models.Model):
    title = models.CharField(max_length=255)  # Заголовок объявления
    content = models.TextField()  # Текст объявления
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор объявления
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания объявления

    def __str__(self):
        return self.title  # Возвращает строковое представление объявления

# Модель для комментария
class Comment(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)  # Объявление, к которому относится комментарий
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор комментария
    content = models.TextField()  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания комментария

    def __str__(self):
        return f'Comment by {self.author} on {self.advertisement}'  # Возвращает строковое представление комментария