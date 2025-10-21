
from django import forms
from .models import Bus, Route, RouteStop, BusSchedule

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['bus_number', 'bus_name', 'capacity', 'bus_type', 'status', 'registration_plate', 'bus_image']
        widgets = {
            'bus_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bus Number'}),
            'bus_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bus Name'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacity'}),
            'bus_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bus Type (AC/Non-AC)'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'registration_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration Plate'}),
            'bus_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['route_name', 'start_point', 'end_point', 'total_distance', 'estimated_duration', 'is_active']
        widgets = {
            'route_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Route Name'}),
            'start_point': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Start Point'}),
            'end_point': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'End Point'}),
            'total_distance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Distance (KM)'}),
            'estimated_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration (Minutes)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BusScheduleForm(forms.ModelForm):
    class Meta:
        model = BusSchedule
        fields = ['bus', 'route', 'shift', 'departure_time', 'arrival_time', 'days_of_week', 'is_active']
        widgets = {
            'bus': forms.Select(attrs={'class': 'form-control'}),
            'route': forms.Select(attrs={'class': 'form-control'}),
            'shift': forms.Select(attrs={'class': 'form-control'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'days_of_week': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., sunday,monday,wednesday'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }