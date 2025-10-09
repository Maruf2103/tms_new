from django.db import models
from django.conf import settings
from buses.models import BusSchedule
from django.core.validators import MinValueValidator
import uuid


class BusRegistration(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    )

    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bus_registrations')
    bus_schedule = models.ForeignKey(BusSchedule, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateField()
    valid_until = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    seat_number = models.CharField(max_length=10, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.bus_schedule.bus.bus_number} ({self.registration_id})"

    class Meta:
        ordering = ['-created_at']


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash'),
    )

    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registration = models.OneToOneField(BusRegistration, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='verified_payments')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.amount} BDT"

    class Meta:
        ordering = ['-payment_date']


class RegistrationHistory(models.Model):
    registration = models.ForeignKey(BusRegistration, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=100)
    description = models.TextField()
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration.registration_id} - {self.action}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Registration Histories'