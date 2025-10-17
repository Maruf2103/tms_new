from django.db import models
from django.conf import settings

class Bus(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=100)
    distance = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.name

class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.bus} - {self.route}"

class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    registration_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.schedule}"
