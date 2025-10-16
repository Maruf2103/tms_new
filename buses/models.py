from django.db import models
from django.core.validators import MinValueValidator



class Bus(models.Model):
    BUS_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
    )

    bus_number = models.CharField(max_length=20, unique=True)
    bus_name = models.CharField(max_length=100)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    bus_type = models.CharField(max_length=50, default='AC')  # AC/Non-AC
    status = models.CharField(max_length=20, choices=BUS_STATUS_CHOICES, default='active')
    registration_plate = models.CharField(max_length=20, unique=True)
    bus_image = models.ImageField(upload_to='bus_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus_number} - {self.bus_name}"

    def available_seats(self):
        """Calculate available seats based on active registrations"""
        from registrations.models import BusRegistration
        active_registrations = BusRegistration.objects.filter(
            bus_schedule__bus=self,
            status='active'
        ).count()
        return self.capacity - active_registrations

    class Meta:
        ordering = ['bus_number']
        verbose_name_plural = 'Buses'


class Route(models.Model):
    route_name = models.CharField(max_length=200)
    start_point = models.CharField(max_length=200)
    end_point = models.CharField(max_length=200)
    total_distance = models.DecimalField(max_digits=6, decimal_places=2, help_text="Distance in KM")
    estimated_duration = models.IntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.route_name} ({self.start_point} - {self.end_point})"

    class Meta:
        ordering = ['route_name']


class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    stop_name = models.CharField(max_length=200)
    stop_order = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.route.route_name} - {self.stop_name}"

    class Meta:
        ordering = ['route', 'stop_order']
        unique_together = ['route', 'stop_order']


class BusSchedule(models.Model):
    SHIFT_CHOICES = (
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    )

    DAY_CHOICES = (
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='schedules')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='schedules')
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    days_of_week = models.CharField(max_length=200, help_text="Comma-separated days: sunday,monday,etc")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus.bus_number} - {self.route.route_name} ({self.shift})"

    def available_seats(self):
        from registrations.models import BusRegistration
        active_registrations = BusRegistration.objects.filter(
            bus_schedule=self,
            status='active'
        ).count()
        return self.bus.capacity - active_registrations

    class Meta:
        ordering = ['departure_time']
        unique_together = ['bus', 'route', 'shift', 'departure_time']