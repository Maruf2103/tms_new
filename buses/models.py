from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone


class Bus(models.Model):
    bus_number = models.CharField(max_length=20, unique=True)
    bus_name = models.CharField(max_length=100)
    capacity = models.IntegerField(default=40)
    driver_name = models.CharField(max_length=100, default='Driver Name')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Bus'
        verbose_name_plural = 'Buses'
        ordering = ['bus_number']

    def __str__(self):
        return f"{self.bus_number} - {self.bus_name}"


class Route(models.Model):
    route_name = models.CharField(max_length=100, default='UAP Route')
    start_point = models.CharField(max_length=255, default='UAP Campus')
    end_point = models.CharField(max_length=255, default='City Center')
    stops = models.TextField(help_text='Comma separated bus stops', default='', blank=True)
    distance = models.FloatField(help_text='Distance in km', default=0)
    estimated_time = models.IntegerField(help_text='Estimated time in minutes', default=0)
    fare = models.DecimalField(max_digits=6, decimal_places=2, default=20.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'
        ordering = ['route_name']

    def __str__(self):
        return f"{self.route_name} ({self.start_point} to {self.end_point})"


class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    available_seats = models.IntegerField(default=40)
    is_active = models.BooleanField(default=True)
    # Use localdate to avoid UTC/local timezone date mismatch when defaulting
    date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f"{self.bus.bus_number} - {self.route.route_name} - {self.departure_time}"


class Booking(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    booking_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bus_bookings')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    passengers = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'Booking {self.booking_id} - {self.user.username}'


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='bus_payments', null=True, blank=True)
    # Link to MonthlySubscription when the payment is for a subscription
    subscription = models.ForeignKey('MonthlySubscription', on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='bkash')
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f'Payment {self.transaction_id} - {self.amount}'


class UserProfile(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('staff', 'Staff'),
        ('authority', 'Transport Authority'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bus_user_profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    student_id = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=15, default='')
    address = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.user_type}'


class MonthlySubscription(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    subscription_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='monthly_subscriptions')
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    passengers = models.IntegerField(default=1)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Whether seats on the related schedule have been reserved for this subscription
    seats_reserved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Monthly Subscription'
        verbose_name_plural = 'Monthly Subscriptions'

    def save(self, *args, **kwargs):
        # If end_date not set, default to 30 days after start_date
        if not self.end_date and self.start_date:
            from datetime import timedelta
            self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Subscription {self.subscription_id} - {self.user.username} ({self.schedule})'
