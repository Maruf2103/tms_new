from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import BusRegistration, Payment, RegistrationHistory

@admin.register(BusRegistration)
class BusRegistrationAdmin(admin.ModelAdmin):
    list_display = ('registration_id', 'user', 'bus_schedule', 'status', 'payment_status', 'valid_from', 'valid_until')
    list_filter = ('status', 'payment_status')
    search_fields = ('registration_id', 'user__username', 'bus_schedule__bus__bus_number')
    readonly_fields = ('registration_id', 'created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'registration', 'amount', 'payment_method', 'is_verified', 'payment_date')
    list_filter = ('payment_method', 'is_verified')
    search_fields = ('payment_id', 'transaction_id')
    readonly_fields = ('payment_id', 'payment_date')

@admin.register(RegistrationHistory)
class RegistrationHistoryAdmin(admin.ModelAdmin):
    list_display = ('registration', 'action', 'performed_by', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('registration__registration_id', 'action')