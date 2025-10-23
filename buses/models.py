from django.db import models

class Bus(models.Model):
    bus_number = models.CharField(max_length=20, unique=True, default='UAP-001')
    bus_name = models.CharField(max_length=100, default='Campus Bus')
    capacity = models.IntegerField(default=40)
    driver_name = models.CharField(max_length=100, default='Driver Name')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bus_number} - {self.bus_name}"

class Route(models.Model):
    route_name = models.CharField(max_length=100, default='UAP Route')
    start_point = models.CharField(max_length=255, default='UAP Campus')
    end_point = models.CharField(max_length=255, default='City Center')
    fare = models.DecimalField(max_digits=6, decimal_places=2, default=20.00)

    def __str__(self):
        return f"{self.route_name}"
