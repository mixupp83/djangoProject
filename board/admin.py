from django.contrib import admin
from .models import Advertisement, Comment, UserProfile

# Регистрация моделей в административной панели Django
admin.site.register(Advertisement)
admin.site.register(Comment)
admin.site.register(UserProfile)