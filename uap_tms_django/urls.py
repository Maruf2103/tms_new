# uap_tms_django/urls.py
from django.contrib import admin
from django.urls import path, include
from transportation import views as transport_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('custom_admin.urls')),
    path('', transport_views.home, name='home'),
    path('login/', transport_views.user_login, name='login'),
    path('signup/', transport_views.signup, name='signup'),
    path('dashboard/', transport_views.dashboard, name='dashboard'),
    path('profile/', transport_views.profile, name='profile'),
    path('live-tracking/', transport_views.live_tracking, name='live_tracking'),
    path('payment/', transport_views.payment_page, name='payment'),
    path('process-payment/', transport_views.process_payment, name='process_payment'),
    path('logout/', transport_views.user_logout, name='logout'),
    path('api/status/', transport_views.api_status, name='api_status'),
    path('bus/register/<int:bus_id>/', transport_views.register_bus, name='register_bus'),
    path('transport/', include('transportation.urls')),  # Keep this for any additional transportation URLs
]
