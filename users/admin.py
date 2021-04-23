from django.contrib import admin

# Register your models here.
from users.models import UserProfile


class UsersAdmin(admin.ModelAdmin):
    list_display = ('nickname','mobile','address')
admin.site.register(UserProfile)