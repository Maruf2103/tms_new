
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import *
import json
from datetime import datetime, date

# =============================================
# USER AUTHENTICATION SYSTEM
# =============================================

def signup(request):
    # User registration/signup view
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type', 'student')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        student_id = request.POST.get('student_id', '')

        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'auth/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'auth/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'auth/signup.html')

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                student_id=student_id,
                phone=phone,
                address=address
            )
            
            messages.success(request, 'Account created successfully! Please sign 
in.')
            return redirect('signin')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'auth/signup.html')
    
    return render(request, 'auth/signup.html')

def signin(request):
    # User login/signin view
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect based on user type
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.user_type == 'authority':
                    return redirect('authority_panel')
                else:
                    return redirect('dashboard')
            except UserProfile.DoesNotExist:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'auth/signin.html')

def sign_out(request):
    # User logout view
    logout(request)
    messages.success(request, 'You have been successfully signed out!')
    return redirect('home')

@login_required
def dashboard(request):
    # User dashboard after login
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, 
user_type='student')
    
    context = {
        'user_profile': user_profile
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile(request):
    # User profile management
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, user_type='student')
    
    if request.method == 'POST':
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.student_id = request.POST.get('student_id', '')
        profile.user_type = request.POST.get('user_type', 'student')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'auth/profile.html', {'profile': profile})

# =============================================
# ADMIN/AUTHORITY PANEL
# =============================================

@login_required
def authority_panel(request):
    # Authority panel for transport management
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'authority':
            messages.error(request, 'Access denied! Authority panel only.')
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Access denied! Please complete your profile.')
        return redirect('profile')
    
    # Get statistics
    total_buses = Bus.objects.count()
    active_buses = Bus.objects.filter(is_active=True).count()
    total_routes = Route.objects.count()
    total_bookings = Booking.objects.count()
    active_bookings = Booking.objects.filter(is_confirmed=True).count()
    
    # Recent bookings
    recent_bookings = Booking.objects.select_related('user', 
'schedule').order_by('-booking_date')[:10]
    
    context = {
        'total_buses': total_buses,
        'active_buses': active_buses,
        'total_routes': total_routes,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'authority/panel.html', context)

@login_required
def manage_buses(request):
    # Manage buses - add, edit, delete
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'authority':
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        return redirect('dashboard')
    
    buses = Bus.objects.all()
    
    if request.method == 'POST':
        bus_number = request.POST.get('bus_number')
        bus_name = request.POST.get('bus_name')
        capacity = request.POST.get('capacity')
        driver_name = request.POST.get('driver_name')

        if Bus.objects.filter(bus_number=bus_number).exists():
            messages.error(request, 'Bus with this number already exists!')
        else:
            Bus.objects.create(
                bus_number=bus_number,
                bus_name=bus_name,
                capacity=capacity,
                driver_name=driver_name,
            )
            messages.success(request, 'Bus added successfully!')

        return redirect('manage_buses')
    
    return render(request, 'authority/manage_buses.html', {'buses': buses})

@login_required
def manage_routes(request):
    # Manage routes
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'authority':
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        return redirect('dashboard')
    
    routes = Route.objects.all()
    
    if request.method == 'POST':
        route_name = request.POST.get('route_name')
        start_point = request.POST.get('start_point')
        end_point = request.POST.get('end_point')
        stops = request.POST.get('stops')
        distance = request.POST.get('distance')
        estimated_time = request.POST.get('estimated_time')
        fare = request.POST.get('fare')
        
        Route.objects.create(
            route_name=route_name,
            start_point=start_point,
            end_point=end_point,
            stops=stops,
            distance=distance,
            estimated_time=estimated_time,
            fare=fare
        )
        messages.success(request, 'Route added successfully!')
        return redirect('manage_routes')
    
    return render(request, 'authority/manage_routes.html', {'routes': routes})

@login_required
def manage_schedules(request):
    # Manage bus schedules
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'authority':
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        return redirect('dashboard')
    
    schedules = Schedule.objects.select_related('bus', 'route').all()
    buses = Bus.objects.filter(is_active=True)
    routes = Route.objects.all()
    
    if request.method == 'POST':
        bus_id = request.POST.get('bus')
        route_id = request.POST.get('route')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        date = request.POST.get('date')
        
        bus = Bus.objects.get(id=bus_id)
        route = Route.objects.get(id=route_id)
        
        Schedule.objects.create(
            bus=bus,
            route=route,
            departure_time=departure_time,
            arrival_time=arrival_time,
            date=date,
            available_seats=bus.capacity
        )
        messages.success(request, 'Schedule added successfully!')
        return redirect('manage_schedules')
    
    context = {
        'schedules': schedules,
        'buses': buses,
        'routes': routes
    }
    return render(request, 'authority/manage_schedules.html', context)

@login_required
def view_bookings(request):
    # View all bookings
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'authority':
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        return redirect('dashboard')
    
    bookings = Booking.objects.select_related('user', 
'schedule').order_by('-booking_date')
    return render(request, 'authority/view_bookings.html', {'bookings': bookings})

# Basic home view
def home(request):
    return render(request, 'home.html')


