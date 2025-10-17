from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

# Check if Profile model exists and is properly defined
try:
    from .models import Profile
    
    class UserAdmin(BaseUserAdmin):
        inlines = []
    
    admin.site.register(User, UserAdmin)
    
except ImportError:
    # If Profile model doesn't exist or has issues, use basic registration
    admin.site.register(User)
    print('Note: Using basic User admin - Profile model not available')
