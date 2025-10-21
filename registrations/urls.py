from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    path('register/', views.register_bus, name='register_bus'),
    path('register/<int:schedule_id>/confirm/', views.confirm_registration, name='confirm_registration'),
    path('payment/<uuid:registration_id>/', views.payment, name='payment'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('detail/<uuid:registration_id>/', views.registration_detail, name='registration_detail'),
    path('cancel/<uuid:registration_id>/', views.cancel_registration, name='cancel_registration'),

    # Authority URLs
    path('all/', views.all_registrations, name='all_registrations'),
]