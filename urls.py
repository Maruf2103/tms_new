from django.contrib import admin
from django.urls import path
from buses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-portal/', views.admin_portal, name='admin_portal'),
    path('admin-signup/', views.admin_signup, name='admin_signup'),
    path('', views.home, name='home'),
    
    # Authentication URLs - Added by Samia
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Authority Panel URLs - Added by Samia
    path('authority-panel/', views.authority_panel, name='authority_panel'),
    path('authority/buses/', views.manage_buses, name='manage_buses'),
    path('authority/routes/', views.manage_routes, name='manage_routes'),
    path('authority/schedules/', views.manage_schedules, name='manage_schedules'),
    path('authority/bookings/', views.view_bookings, name='view_bookings'),
    
    # Bus Registration URLs - Added by Zakir
    path('bus-registration/', views.bus_registration, name='bus_registration'),
    path('search-routes/', views.search_routes, name='search_routes'),
    path('select-bus/', views.select_bus, name='select_bus'),
    path('payment/', views.payment, name='payment'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
