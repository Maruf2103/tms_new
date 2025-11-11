from django.contrib import admin
from .models import Bus, Route, Schedule, Booking, Payment, UserProfile, MonthlySubscription

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'bus_name', 'capacity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('bus_number', 'bus_name')
    list_editable = ('is_active',)
    list_per_page = 20

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_name', 'start_point', 'end_point', 'fare', 'estimated_time')
    search_fields = ('route_name', 'start_point', 'end_point')
    list_filter = ('fare',)
    list_per_page = 20

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('bus', 'route', 'date', 'departure_time', 'arrival_time', 'available_seats', 'is_active')
    list_filter = ('date', 'is_active', 'bus', 'route')
    search_fields = ('bus__bus_number', 'route__route_name')
    date_hierarchy = 'date'
    list_editable = ('is_active',)
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('bus', 'route')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'schedule', 'booking_date', 'passengers', 'total_amount', 'payment_status', 'is_confirmed')
    list_filter = ('booking_date', 'payment_status', 'is_confirmed')
    search_fields = ('booking_id', 'user__username', 'schedule__bus__bus_number')
    date_hierarchy = 'booking_date'
    readonly_fields = ('booking_id',)
    list_editable = ('is_confirmed',)
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'schedule', 'schedule__bus', 'schedule__route')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'booking', 'amount', 'payment_method', 'payment_date', 'status')
    list_filter = ('payment_date', 'payment_method', 'status')
    search_fields = ('transaction_id', 'booking__booking_id')
    date_hierarchy = 'payment_date'
    readonly_fields = ('transaction_id',)
    list_editable = ('status',)
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('booking', 'booking__user')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'student_id', 'phone', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'student_id', 'phone')
    date_hierarchy = 'created_at'
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(MonthlySubscription)
class MonthlySubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscription_id', 'user', 'schedule', 'start_date', 'end_date', 'passengers', 'monthly_amount', 'payment_status', 'is_active', 'created_at')
    list_filter = ('payment_status', 'is_active', 'start_date')
    search_fields = ('subscription_id', 'user__username', 'schedule__bus__bus_number')
    date_hierarchy = 'created_at'
    readonly_fields = ('subscription_id',)
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'schedule', 'schedule__bus', 'schedule__route')