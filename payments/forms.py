from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'pattern': '[0-9]{16}'
        }),
        label="Card Number"
    )
    expiry_month = forms.ChoiceField(
        choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    expiry_year = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(2024, 2035)],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '123'}),
        label="CVV"
    )