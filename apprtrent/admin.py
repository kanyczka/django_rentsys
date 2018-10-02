from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Owner, Appartment, Photo, Booking, City, Fee, Article, Facility

# from apprtrent.models import

# Register your models here.


admin.site.register(User, UserAdmin)
admin.site.register(Owner)
admin.site.register(Appartment)
admin.site.register(Photo)
admin.site.register(Booking)
admin.site.register(City)
admin.site.register(Fee)
admin.site.register(Article)
admin.site.register(Facility)


