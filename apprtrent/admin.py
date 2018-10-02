from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# from apprtrent.models import

# Register your models here.


admin.site.register(User, UserAdmin)
