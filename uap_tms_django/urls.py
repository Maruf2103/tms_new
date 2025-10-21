from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from . import views

# Root level redirect for /login/ to /transport/login/
def root_login_redirect(request):
    return redirect('/transport/login/')

# Root level redirect for admin login
def admin_login_redirect(request):
    return redirect('/transport/login/?next=/admin-panel/dashboard/')

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # Root level redirects
    path('login/', root_login_redirect),
    path('admin/login/', admin_login_redirect),
    
    # Admin panel routes
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/buses/', views.admin_buses, name='admin_buses'),
    path('admin-panel/analytics/', views.admin_analytics, name='admin_analytics'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    # Transport app routes
    path('transport/', views.home_view, name='home'),
    path('transport/signup/', views.signup_view, name='signup'),
    path('transport/login/', views.login_view, name='login'),
    path('transport/dashboard/', views.dashboard_view, name='dashboard'),
    path('transport/logout/', views.logout_view, name='logout'),
    path('transport/api/status/', views.api_status, name='api_status'),
]


