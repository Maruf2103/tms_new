from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()

if apps.is_installed('accounts.Profile'):
    from .models import Profile

    class UserAdmin(BaseUserAdmin):
        inlines = []

    admin.site.register(User, UserAdmin)
else:
    admin.site.register(User)
    print('Note: Using basic User admin - Profile model not available')
