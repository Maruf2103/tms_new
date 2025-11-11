from django.contrib import admin
from django.urls import path
from buses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('bus-registration/', views.bus_registration, name='bus_registration'),
    path('search-routes/', views.search_routes, name='search_routes'),
    path('view-schedules/', views.view_schedules, name='view_schedules'),
    path('bus-schedule/', views.bus_schedule, name='bus_schedule'),
    path('book-bus/<int:schedule_id>/', views.book_bus, name='book_bus'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-checkout/', views.process_checkout, name='process_checkout'),
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('cancel-booking/<uuid:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('cancel-subscription/<uuid:subscription_id>/', views.cancel_subscription, name='cancel_subscription'),
    path('subscription/<uuid:subscription_id>/', views.subscription_detail, name='subscription_detail'),
    path('booking/<uuid:booking_id>/', views.booking_details, name='booking_details'),
    
    # Admin management URLs
    path('manage-buses/', views.manage_buses, name='manage_buses'),
    path('manage-schedules/', views.manage_schedules, name='manage_schedules'),
    path('edit-schedule/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('toggle-schedule/<int:schedule_id>/', views.toggle_schedule, name='toggle_schedule'),
]
