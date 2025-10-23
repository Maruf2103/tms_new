from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

# Basic views for now
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1)
                login(request, user)
                messages.success(request, 'Account created successfully! Please sign in.')
                return redirect('dashboard')
            except:
                messages.error(request, 'Username already exists!')
        else:
            messages.error(request, 'Passwords do not match!')
    
    return render(request, 'auth/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'auth/signin.html')

def sign_out(request):
    logout(request)
    messages.success(request, 'You have been signed out!')
    return redirect('home')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, 'Thank you for your message!')
        return redirect('contact_us')
    
    return render(request, 'contact_us.html')

# Bus registration views
@login_required
def bus_registration(request):
    return render(request, 'bus/registration.html')

@login_required
def search_routes(request):
    if request.method == 'POST':
        start_point = request.POST.get('start_point')
        end_point = request.POST.get('end_point')
        messages.info(request, f'Searching routes from {start_point} to {end_point}')
        return render(request, 'bus/search_results.html')
    
    return render(request, 'bus/search_routes.html')

@login_required
def select_bus(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        time_slot = request.POST.get('time_slot')
        messages.success(request, f'Selected bus {bus_id} at {time_slot}')
        return redirect('make_payment')
    
    return render(request, 'bus/select_bus.html')

@login_required
def make_payment(request):
    if request.method == 'POST':
        messages.success(request, 'Payment completed successfully!')
        return redirect('booking_confirmation')
    
    return render(request, 'bus/payment.html')

@login_required
def booking_confirmation(request):
    return render(request, 'bus/confirmation.html')
