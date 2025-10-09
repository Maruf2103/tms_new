from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Buses, Route, RouteStop, BusSchedule

class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1

@admin.register(Buses)
class BusesAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'bus_name', 'capacity', 'bus_type', 'status', 'registration_plate')
    list_filter = ('status', 'bus_type')
    search_fields = ('bus_number', 'bus_name', 'registration_plate')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_name', 'start_point', 'end_point', 'total_distance', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('route_name', 'start_point', 'end_point')
    inlines = [RouteStopInline]

@admin.register(BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ('bus', 'route', 'shift', 'departure_time', 'arrival_time', 'is_active')
    list_filter = ('shift', 'is_active')
    search_fields = ('bus__bus_number', 'route__route_name')

