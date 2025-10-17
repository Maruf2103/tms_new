# transportation/admin.py
from django.contrib import admin
from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'department', 'phone']
    list_filter = ['user_type', 'department']

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'route', 'departure_time', 'available_seats', 'status']
    list_filter = ['status']

@admin.register(BusRegistration)
class BusRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'bus', 'travel_date', 'status', 'payment_status']
    list_filter = ['status', 'payment_status']

admin.site.register(Route)
admin.site.register(Payment)
admin.site.register(BusLocation)
