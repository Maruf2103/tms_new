# transportation/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('staff', 'Staff'),
        ('admin', 'Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user_type})"

class Bus(models.Model):
    bus_number = models.CharField(max_length=20, unique=True)
    route = models.CharField(max_length=200)
    departure_time = models.CharField(max_length=50)  # Using CharField for simplicity
    capacity = models.IntegerField(default=40, validators=[MinValueValidator(1), MaxValueValidator(100)])
    available_seats = models.IntegerField(default=40)
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('maintenance', 'Maintenance')], default='active')
    
    def __str__(self):
        return f"{self.bus_number} - {self.route}"

class BusRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField(auto_now_add=True)  # Using auto_now_add for simplicity
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        unique_together = ['user', 'bus', 'travel_date']
    
    def __str__(self):
        return f"{self.user.user.get_full_name()} - {self.bus.bus_number}"

class Payment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')])
    payment_date = models.DateTimeField(auto_now_add=True)
    bus_registration = models.ForeignKey(BusRegistration, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.user.user.get_full_name()}"
