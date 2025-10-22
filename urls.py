from django.contrib import admin
from django.urls import path, include
from transportation import views as transportation_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom-admin/', include('custom_admin.urls')),
    path('', transportation_views.home_view, name='home'),
    path('login/', transportation_views.login_view, name='login'),
    path('logout/', transportation_views.logout_view, name='logout'),
    path('signup/', transportation_views.signup_view, name='signup'),
    path('dashboard/', transportation_views.dashboard_view, name='dashboard'),
    path('transportation/', include('transportation.urls')),
]
