from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('make/<int:bus_id>/', views.make_payment, name='make_payment'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
]