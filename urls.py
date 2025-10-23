from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from transportation import views as transport_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('custom_admin.urls')),
    path('transport/', include('transportation.urls')),
    path('', transport_views.home, name='home'),
    path('login/', transport_views.user_login, name='login'),
    path('signup/', transport_views.signup, name='signup'),
]
