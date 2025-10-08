from django.contrib import admin
from .models import BusLocation, BusStatus, Notification

@admin.register(BusLocation)
class BusLocationAdmin(admin.ModelAdmin):
    list_display = ('bus', 'latitude', 'longitude', 'speed', 'timestamp', 'is_active')
    list_filter = ('is_active', 'timestamp')
    search_fields = ('bus__bus_number',)
    readonly_fields = ('timestamp',)

@admin.register(BusStatus)
class BusStatusAdmin(admin.ModelAdmin):
    list_display = ('bus', 'status', 'current_stop', 'delay_minutes', 'last_updated')
    list_filter = ('status',)
    search_fields = ('bus__bus_number', 'current_stop')
    readonly_fields = ('last_updated',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('bus', 'notification_type', 'title', 'created_at', 'is_active')
    list_filter = ('notification_type', 'is_active', 'created_at')
    search_fields = ('bus__bus_number', 'title', 'message')
    readonly_fields = ('created_at',)