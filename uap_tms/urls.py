from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Authentication URLs - using Django's built-in auth views
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/signup/', TemplateView.as_view(template_name='accounts/signup.html'), name='signup'),
    path('accounts/register/', TemplateView.as_view(template_name='accounts/register.html'), name='register'),
    
    # Include app URLs but keep them commented out until we fix the import issues
    # path('buses/', include('buses.urls')),
    # path('tracking/', include('tracking.urls')),
    # path('registrations/', include('registrations.urls')),
    # path('accounts/', include('accounts.urls')),
]

# Debug toolbar (optional)
from django.conf import settings
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    except ImportError:
        pass
