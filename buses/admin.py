from django.contrib import admin
from .models import Bus, Route, BusSchedule, Registration

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ["id", "bus_number"]
    search_fields = ["bus_number"]

@admin.register(Route)  
class RouteAdmin(admin.ModelAdmin):
    list_display = ["id", "route_name"]

@admin.register(BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ["id", "bus"]

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ["id"]
