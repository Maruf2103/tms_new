# transportation/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from datetime import datetime, date
import json

def home(request):
    """Home page"""
    return render(request, 'transportation/index.html')

def signup(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department', '')
        student_id = request.POST.get('student_id', '')

        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'transportation/signup.html')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long!')
            return render(request, 'transportation/signup.html')

        try:
            # Create Django user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=full_name
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                phone=phone,
                department=department,
                student_id=student_id if user_type == 'student' else None
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Registration error: {str(e)}')

    return render(request, 'transportation/signup.html')

def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            
            # Redirect to admin if staff user
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'transportation/login.html')

@login_required
def dashboard(request):
    """User dashboard"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    # Get available buses for today
    today = date.today()
    available_buses = Bus.objects.filter(
        status='active',
        available_seats__gt=0
    )
    
    # Get user's registrations
    user_registrations = BusRegistration.objects.filter(
        user=user_profile
    ).select_related('bus').order_by('-registration_date') if user_profile else []
    
    context = {
        'user_profile': user_profile,
        'available_buses': available_buses,
        'user_registrations': user_registrations,
        'today': today,
    }
    return render(request, 'transportation/dashboard.html', context)

@login_required
def register_bus(request, bus_id):
    """Register for a bus"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        bus = Bus.objects.get(id=bus_id)
        
        # Check if already registered for today
        today = date.today()
        existing_registration = BusRegistration.objects.filter(
            user=user_profile,
            bus=bus,
            travel_date=today
        ).exists()
        
        if existing_registration:
            messages.warning(request, 'You are already registered for this bus today!')
        elif bus.available_seats <= 0:
            messages.error(request, 'No available seats on this bus!')
        else:
            # Create registration
            BusRegistration.objects.create(
                user=user_profile,
                bus=bus,
                travel_date=today,
                status='confirmed'
            )
            
            # Update available seats
            bus.available_seats -= 1
            bus.save()
            
            messages.success(request, f'Successfully registered for {bus.bus_number}!')
            
    except Exception as e:
        messages.error(request, f'Registration error: {str(e)}')
    
    return redirect('dashboard')

@login_required
def profile(request):
    """User profile"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'transportation/profile.html', context)

@login_required
def live_tracking(request):
    """Live bus tracking"""
    buses = Bus.objects.filter(status='active')
    
    # Simulate bus locations (in real app, this would come from GPS)
    bus_locations = []
    for bus in buses:
        bus_locations.append({
            'bus_number': bus.bus_number,
            'route': bus.route,
            'driver': bus.driver_name,
            'lat': 23.7806 + (int(bus.id) * 0.001),  # Simulated coordinates
            'lng': 90.4193 + (int(bus.id) * 0.001),
            'status': 'moving'
        })
    
    context = {
        'buses': buses,
        'bus_locations': json.dumps(bus_locations),
    }
    return render(request, 'transportation/live_tracking.html', context)

@login_required
def payment_page(request):
    """Payment page"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        pending_payments = BusRegistration.objects.filter(
            user=user_profile,
            payment_status='pending'
        )
    except UserProfile.DoesNotExist:
        pending_payments = []
    
    context = {
        'pending_payments': pending_payments,
    }
    return render(request, 'transportation/payment.html', context)

@login_required
def process_payment(request):
    """Process payment"""
    if request.method == 'POST':
        registration_id = request.POST.get('registration_id')
        payment_method = request.POST.get('payment_method')
        
        try:
            registration = BusRegistration.objects.get(id=registration_id)
            
            # Create payment record
            Payment.objects.create(
                user=registration.user,
                amount=50.00,  # Fixed bus fare
                payment_method=payment_method,
                transaction_id=f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}",
                status='success',
                bus_registration=registration
            )
            
            # Update registration payment status
            registration.payment_status = 'paid'
            registration.payment_method = payment_method
            registration.save()
            
            messages.success(request, 'Payment processed successfully!')
            
        except Exception as e:
            messages.error(request, f'Payment error: {str(e)}')
    
    return redirect('dashboard')

def user_logout(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')

def api_status(request):
    """API status"""
    return JsonResponse({
        "status": "operational",
        "service": "UAP-TMS Django",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
    })
