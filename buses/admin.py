from django.contrib import admin
from .models import Bus, BusSchedule, Route, Registration

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'route_name', 'capacity', 'is_active']
    list_filter = ['is_active', 'route_name']

@admin.register(BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ['bus', 'departure_time', 'arrival_time', 'available_seats']
    list_filter = ['bus__route_name']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['route_name', 'start_point', 'end_point']

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'bus_schedule', 'registration_date', 'payment_status']
    list_filter = ['payment_status', 'registration_date']