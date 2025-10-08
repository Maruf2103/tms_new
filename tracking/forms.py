from django import forms
from .models import BusLocation, BusStatus, Notification

class BusLocationForm(forms.ModelForm):
    class Meta:
        model = BusLocation
        fields = ['bus', 'latitude', 'longitude', 'speed', 'heading']
        widgets = {
            'bus': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001', 'placeholder': 'Longitude'}),
            'speed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Speed (km/h)'}),
            'heading': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Heading (degrees)'}),
        }

class BusStatusForm(forms.ModelForm):
    class Meta:
        model = BusStatus
        fields = ['bus', 'status', 'current_stop', 'estimated_arrival', 'delay_minutes', 'notes']
        widgets = {
            'bus': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'current_stop': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Stop'}),
            'estimated_arrival': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'delay_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Delay in minutes'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Status notes...'}),
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['bus', 'notification_type', 'title', 'message', 'is_active']
        widgets = {
            'bus': forms.Select(attrs={'class': 'form-control'}),
            'notification_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notification Title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Notification Message'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }