# transportation/admin.py
from django.contrib import admin
from .models import UserProfile, Bus, BusRegistration, Payment

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
    list_display = ['user', 'bus', 'registration_date', 'status', 'payment_status']
    list_filter = ['status', 'payment_status']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'status', 'payment_date']
    list_filter = ['status', 'payment_method']
# ADD TO transportation/admin.py (after the imports)
from .models import UserProfile, Bus, BusRegistration, Payment, Route

# ADD THIS LINE after the other admin registrations
admin.site.register(Route)
