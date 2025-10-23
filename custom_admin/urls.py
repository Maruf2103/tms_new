# custom_admin/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('bus-management/', views.admin_bus_management, name='admin_bus_management'),
    path('user-management/', views.admin_user_management, name='admin_user_management'),
    path('registration-management/', views.admin_registration_management, name='admin_registration_management'),
    path('reports/', views.admin_reports, name='admin_reports'),
    path('settings/', views.admin_system_settings, name='admin_settings'),
    path('api/data/', views.admin_api_data, name='admin_api_data'),
]
