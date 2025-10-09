from django.urls import path
from . import views

app_name = 'buses'

urlpatterns = [
    path('', views.bus_list, name='bus_list'),
    path('<int:bus_id>/', views.bus_detail, name='bus_detail'),
    path('routes/', views.route_list, name='route_list'),
    path('schedules/', views.schedule_list, name='schedule_list'),

    # Authority URLs
    path('manage/', views.manage_buses, name='manage_buses'),
    path('add/', views.add_bus, name='add_bus'),
    path('<int:bus_id>/edit/', views.edit_bus, name='edit_bus'),
    path('<int:bus_id>/delete/', views.delete_bus, name='delete_bus'),
    path('schedule/add/', views.add_schedule, name='add_schedule'),
]