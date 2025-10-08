from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.live_tracking, name='live_tracking'),
    path('bus/<int:bus_id>/', views.bus_tracking_detail, name='bus_tracking_detail'),
    path('api/bus/<int:bus_id>/location/', views.get_bus_location_api, name='get_bus_location_api'),
    path('notifications/', views.notifications_list, name='notifications_list'),
    
    # Authority URLs
    path('manage/', views.manage_tracking, name='manage_tracking'),
    path('update-location/', views.update_location, name='update_location'),
    path('update-status/', views.update_status, name='update_status'),
    path('update-status/<int:bus_id>/', views.update_status, name='update_status_bus'),
    path('create-notification/', views.create_notification, name='create_notification'),
]