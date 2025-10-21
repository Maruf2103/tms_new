from django import forms

from buses.models import BusSchedule
from .models import BusRegistration, Payment
from datetime import date, timedelta


class BusRegistrationForm(forms.ModelForm):
    class Meta:
        model = BusRegistration
        fields = ['bus_schedule', 'valid_from', 'valid_until', 'notes']
        widgets = {
            'bus_schedule': forms.Select(attrs={'class': 'form-control'}),
            'valid_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valid_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requirements...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default dates
        if not self.instance.pk:
            self.fields['valid_from'].initial = date.today()
            self.fields['valid_until'].initial = date.today() + timedelta(days=30)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount', 'transaction_id', 'notes']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Amount in BDT', 'readonly': 'readonly'}),
            'transaction_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Transaction ID (if applicable)'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Payment notes...'}),
        }


class SearchBusForm(forms.Form):
    route = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Route"
    )
    shift = forms.ChoiceField(
        choices=[('', 'Select Shift')] + list(BusSchedule.SHIFT_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from buses.models import Route
        self.fields['route'].queryset = Route.objects.filter(is_active=True)