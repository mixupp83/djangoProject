from django.contrib import admin
from .models import Advertisement, Comment

# Регистрация моделей Advertisement и Comment в административной панели Django
admin.site.register(Advertisement)
admin.site.register(Comment)
