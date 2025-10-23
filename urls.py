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
    path('select-bus/', views.select_bus, name='select_bus'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
]
