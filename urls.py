from django.contrib import admin
from django.urls import path
from buses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Authority Panel URLs
    path('authority-panel/', views.authority_panel, name='authority_panel'),
    path('authority/buses/', views.manage_buses, name='manage_buses'),
    path('authority/routes/', views.manage_routes, name='manage_routes'),
    path('authority/schedules/', views.manage_schedules, name='manage_schedules'),
    path('authority/bookings/', views.view_bookings, name='view_bookings'),
    
    # Add other existing URLs here
]
