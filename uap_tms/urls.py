from django.contrib import admin
from django.urls import path
from buses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-portal/', views.admin_portal, name='admin_portal'),
    path('admin-signup/', views.admin_signup, name='admin_signup'),
    path('admin-signin/', views.admin_signin, name='admin_signin'),
    path('', views.home, name='home'),
    path('authority-panel/', views.authority_panel, name='authority_panel'),
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
    path('manage-routes/', views.manage_routes, name='manage_routes'),
    path('manage-schedules/', views.manage_schedules, name='manage_schedules'),
    path('edit-schedule/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('toggle-schedule/<int:schedule_id>/', views.toggle_schedule, name='toggle_schedule'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('toggle-user-active/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]
