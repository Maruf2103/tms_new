from django.shortcuts import render
from django.http import HttpResponse

def home_view(request):
    return render(request, 'home.html')  # or your template name

def signup_view(request):
    return render(request, 'signup.html')

def login_view(request):
    return render(request, 'login.html')
