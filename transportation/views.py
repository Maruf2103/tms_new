from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home_view(request):
    return HttpResponse('
        <h1>Welcome to TMS</h1>
        <a href=\"/login/\">Login</a> | 
        <a href=\"/signup/\">Sign Up</a> |
        <a href=\"/dashboard/\">Dashboard</a>
    ')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse('Invalid login')
    
    return HttpResponse('
        <h2>Login</h2>
        <form method=\"post\">
            <input type=\"text\" name=\"username\" placeholder=\"Username\" required><br>
            <input type=\"password\" name=\"password\" placeholder=\"Password\" required><br>
            <button type=\"submit\">Login</button>
        </form>
        <a href=\"/signup/\">Don\'t have an account? Sign up</a>
    ')

def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    
    form = UserCreationForm()
    return HttpResponse(f'
        <h2>Sign Up</h2>
        <form method=\"post\">
            <input type=\"text\" name=\"username\" placeholder=\"Username\" required><br>
            <input type=\"password\" name=\"password1\" placeholder=\"Password\" required><br>
            <input type=\"password\" name=\"password2\" placeholder=\"Confirm Password\" required><br>
            <button type=\"submit\">Sign Up</button>
        </form>
        <a href=\"/login/\">Already have an account? Login</a>
    ')

@login_required
def dashboard_view(request):
    return HttpResponse(f'
        <h2>Dashboard</h2>
        <p>Welcome, {request.user.username}!</p>
        <a href=\"/logout/\">Logout</a>
    ')
# ADD THIS TO transportation/views.py (replace home function if exists)

def home(request):
    """Home page with features"""
    context = {
        'features': [
            {
                'icon': '📍',
                'title': 'Live Bus Tracking',
                'description': 'Real-time GPS tracking of all university buses'
            },
            {
                'icon': '💳', 
                'title': 'Online Payment',
                'description': 'Secure digital payments with multiple methods'
            },
            {
                'icon': '🛣️',
                'title': 'Smart Routing', 
                'description': 'AI-powered route optimization and suggestions'
            },
            {
                'icon': '👥',
                'title': 'User Management',
                'description': 'Complete authentication system for all users'
            },
            {
                'icon': '📊',
                'title': 'Real-time Analytics',
                'description': 'Comprehensive dashboard with live statistics'
            },
            {
                'icon': '🔔',
                'title': 'Instant Notifications',
                'description': 'Real-time alerts and updates'
            }
        ]
    }
    return render(request, 'transportation/index.html', context)
