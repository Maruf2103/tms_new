from django.db import models
from buses.models import Buses
from django.utils import timezone

class BusLocation(models.Model):
    bus = models.ForeignKey(Buses, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Speed in km/h")
    heading = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Direction in degrees")
    timestamp = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.bus.bus_number} - {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'


class BusStatus(models.Model):
    STATUS_CHOICES = (
        ('on_route', 'On Route'),
        ('at_stop', 'At Stop'),
        ('delayed', 'Delayed'),
        ('breakdown', 'Breakdown'),
        ('not_running', 'Not Running'),
    )
    
    bus = models.OneToOneField(Buses, on_delete=models.CASCADE, related_name='current_status')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_running')
    current_stop = models.CharField(max_length=200, blank=True)
    estimated_arrival = models.TimeField(null=True, blank=True)
    delay_minutes = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.bus.bus_number} - {self.get_status_display()}"
    
    class Meta:
        verbose_name_plural = 'Bus Statuses'


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('delay', 'Delay'),
        ('cancellation', 'Cancellation'),
        ('route_change', 'Route Change'),
        ('general', 'General'),
    )
    
    bus = models.ForeignKey(Buses, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.bus.bus_number} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']