from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Модель для профиля пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Связь с пользователем
    advertisements_count = models.PositiveIntegerField(default=0)  # Количество созданных объявлений
    total_likes = models.PositiveIntegerField(default=0)  # Общее количество лайков
    total_dislikes = models.PositiveIntegerField(default=0)  # Общее количество дизлайков

    def __str__(self):
        return f"Profile of {self.user.username}"

# Модель для объявления
class Advertisement(models.Model):
    title = models.CharField(max_length=255)  # Заголовок объявления
    content = models.TextField()  # Текст объявления
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements')  # Автор объявления
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания объявления
    image = models.ImageField(upload_to='advertisements/', blank=True, null=True)  # Изображение объявления
    likes = models.PositiveIntegerField(default=0)  # Количество лайков
    dislikes = models.PositiveIntegerField(default=0)  # Количество дизлайков

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

# Сигнал для автоматического создания профиля пользователя при создании пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Сигнал для обновления статистики при создании объявления
@receiver(post_save, sender=Advertisement)
def update_advertisements_count_on_create(sender, instance, created, **kwargs):
    if created:
        profile = instance.author.profile
        profile.advertisements_count += 1
        profile.save()

# Сигнал для обновления статистики при удалении объявления
@receiver(post_delete, sender=Advertisement)
def update_advertisements_count_on_delete(sender, instance, **kwargs):
    profile = instance.author.profile
    profile.advertisements_count -= 1
    profile.save()

# Сигнал для обновления статистики при лайке
@receiver(post_save, sender=Advertisement)
def update_likes_count(sender, instance, **kwargs):
    profile = instance.author.profile
    profile.total_likes = instance.likes
    profile.save()

# Сигнал для обновления статистики при дизлайке
@receiver(post_save, sender=Advertisement)
def update_dislikes_count(sender, instance, **kwargs):
    profile = instance.author.profile
    profile.total_dislikes = instance.dislikes
    profile.save()