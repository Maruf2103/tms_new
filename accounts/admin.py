

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from django.contrib import admin
from .models import Profile

class ProfileInline(admin.StackedInline):   # ✅ Must inherit from InlineModelAdmin subclass
    model = Profile



from accounts.admin import ProfileInline

from accounts.models import Profile

from .models import User,Profile

class Profile(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('full_name', 'user_id', 'department', 'address', 'emergency_contact', 'profile_picture', 'is_profile_complete')

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'email')}),
    )
    inlines = [ProfileInline]
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)
#admin.site.register(Profile)
