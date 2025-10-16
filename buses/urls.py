from django.urls import path
from . import views

app_name = 'buses'  # This defines the namespace

urlpatterns = [
    path('registration/', views.bus_registration_view, name='bus_registration'),
    path('complete-profile/', views.complete_profile_view, name='complete_profile'),
    path('payment/<int:registration_id>/', views.payment_view, name='payment'),
    path('schedules/', views.view_schedules, name='view_schedules'),
    path('routes/', views.view_routes, name='view_routes'),
    path('my-registrations/', views.my_registrations_view, name='my_registrations'),
]