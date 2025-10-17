from django.contrib import admin
from django.urls import path, include, include
from django.views.generic import TemplateView

urlpatterns = [
    path('buses/', include('buses.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('bus/', include('bus.urls')),
    path('tracking/', include('tracking.urls')),
]