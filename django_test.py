# django_test.py
import sys
from django.core.management import execute_from_command_line
from django.conf import settings
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>🎉 Django Server Working!</h1><p>TMS can use Django instead of Flask</p>')

def login(request):
    return HttpResponse('<h2>Login Page</h2><form><input><button>Login</button></form>')

urlpatterns = [
    path('', home),
    path('login/', login),
]

if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        SECRET_KEY='secret',
    )

if __name__ == '__main__':
    execute_from_command_line(['manage.py', 'runserver', '8000'])
