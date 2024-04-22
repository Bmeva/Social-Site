from django.contrib import admin
from .models import User, Profile

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'full_name', 'username',  'gender', 'last_login']
    list_editable = ['username', 'gender']
    list_display_links = ['id', 'email']
    ordering = ['id']


class profileAdmin(admin.ModelAdmin):
    list_display = ['id', 'pid', 'full_name', 'user', 'gender', 'phone']
    list_editable = ['full_name', 'gender']
    list_display_links = ['id',]
    ordering = ['id']

admin.site.register(User, UserAdmin)

admin.site.register(Profile, profileAdmin)