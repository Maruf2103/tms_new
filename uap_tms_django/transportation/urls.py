# transportation/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bus/register/<int:bus_id>/', views.register_bus, name='register_bus'),
    path('profile/', views.profile, name='profile'),
    path('live-tracking/', views.live_tracking, name='live_tracking'),
    path('payment/', views.payment_page, name='payment'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('logout/', views.user_logout, name='logout'),
    path('api/status/', views.api_status, name='api_status'),
]
