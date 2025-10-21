# uap_tms_django/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_home(request):
    return redirect('home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('custom_admin.urls')),
    path('transport/', include('transportation.urls')),
    path('', redirect_to_home),
]
