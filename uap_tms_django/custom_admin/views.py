# custom_admin/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from transportation.models import *
from django.db.models import Count, Q
from datetime import datetime, timedelta
import json

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Custom Admin Dashboard"""
    # Statistics
    total_users = UserProfile.objects.count()
    total_buses = Bus.objects.count()
    active_registrations = BusRegistration.objects.filter(status='confirmed').count()
    pending_payments = BusRegistration.objects.filter(payment_status='pending').count()
    
    # Recent registrations
    recent_registrations = BusRegistration.objects.select_related('user', 'bus').order_by('-registration_date')[:10]
    
    # Bus status
    bus_status = Bus.objects.values('status').annotate(count=Count('id'))
    
    context = {
        'total_users': total_users,
        'total_buses': total_buses,
        'active_registrations': active_registrations,
        'pending_payments': pending_payments,
        'recent_registrations': recent_registrations,
        'bus_status': bus_status,
    }
    return render(request, 'custom_admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_bus_management(request):
    """Bus Management View"""
    buses = Bus.objects.all().order_by('bus_number')
    
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        action = request.POST.get('action')
        
        try:
            bus = Bus.objects.get(id=bus_id)
            if action == 'activate':
                bus.status = 'active'
                messages.success(request, f'Bus {bus.bus_number} activated successfully!')
            elif action == 'maintenance':
                bus.status = 'maintenance'
                messages.success(request, f'Bus {bus.bus_number} marked for maintenance!')
            elif action == 'delete':
                bus.delete()
                messages.success(request, f'Bus {bus.bus_number} deleted successfully!')
                return redirect('admin_bus_management')
            
            bus.save()
        except Bus.DoesNotExist:
            messages.error(request, 'Bus not found!')
    
    context = {
        'buses': buses,
    }
    return render(request, 'custom_admin/bus_management.html', context)

@login_required
@user_passes_test(is_admin)
def admin_user_management(request):
    """User Management View"""
    users = UserProfile.objects.select_related('user').all()
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        
        try:
            user_profile = UserProfile.objects.get(id=user_id)
            if action == 'make_faculty':
                user_profile.user_type = 'faculty'
                messages.success(request, f'{user_profile.user.get_full_name()} promoted to faculty!')
            elif action == 'make_student':
                user_profile.user_type = 'student'
                messages.success(request, f'{user_profile.user.get_full_name()} set as student!')
            elif action == 'deactivate':
                user_profile.user.is_active = False
                user_profile.user.save()
                messages.success(request, f'{user_profile.user.get_full_name()} deactivated!')
            elif action == 'activate':
                user_profile.user.is_active = True
                user_profile.user.save()
                messages.success(request, f'{user_profile.user.get_full_name()} activated!')
            
            user_profile.save()
        except UserProfile.DoesNotExist:
            messages.error(request, 'User not found!')
    
    context = {
        'users': users,
    }
    return render(request, 'custom_admin/user_management.html', context)

@login_required
@user_passes_test(is_admin)
def admin_registration_management(request):
    """Registration Management View"""
    registrations = BusRegistration.objects.select_related('user', 'bus').all().order_by('-registration_date')
    
    if request.method == 'POST':
        registration_id = request.POST.get('registration_id')
        action = request.POST.get('action')
        
        try:
            registration = BusRegistration.objects.get(id=registration_id)
            if action == 'confirm':
                registration.status = 'confirmed'
                messages.success(request, 'Registration confirmed!')
            elif action == 'cancel':
                registration.status = 'cancelled'
                # Free up the seat
                registration.bus.available_seats += 1
                registration.bus.save()
                messages.success(request, 'Registration cancelled!')
            elif action == 'mark_paid':
                registration.payment_status = 'paid'
                messages.success(request, 'Payment marked as paid!')
            
            registration.save()
        except BusRegistration.DoesNotExist:
            messages.error(request, 'Registration not found!')
    
    context = {
        'registrations': registrations,
    }
    return render(request, 'custom_admin/registration_management.html', context)

@login_required
@user_passes_test(is_admin)
def admin_reports(request):
    """Reports and Analytics View"""
    # Date range for reports (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Registration statistics
    daily_registrations = BusRegistration.objects.filter(
        registration_date__range=[start_date, end_date]
    ).extra({'date': "date(registration_date)"}).values('date').annotate(count=Count('id'))
    
    # User type distribution
    user_distribution = UserProfile.objects.values('user_type').annotate(count=Count('id'))
    
    # Bus utilization
    bus_utilization = Bus.objects.annotate(
        registration_count=Count('busregistration')
    ).values('bus_number', 'registration_count')
    
    # Payment statistics
    payment_stats = BusRegistration.objects.values('payment_status').annotate(count=Count('id'))
    
    context = {
        'daily_registrations': list(daily_registrations),
        'user_distribution': list(user_distribution),
        'bus_utilization': list(bus_utilization),
        'payment_stats': list(payment_stats),
        'start_date': start_date.date(),
        'end_date': end_date.date(),
    }
    return render(request, 'custom_admin/reports.html', context)

@login_required
@user_passes_test(is_admin)
def admin_system_settings(request):
    """System Settings View"""
    if request.method == 'POST':
        # Handle settings update
        messages.success(request, 'Settings updated successfully!')
    
    return render(request, 'custom_admin/settings.html')

@login_required
@user_passes_test(is_admin)
def admin_api_data(request):
    """API Data for Admin Dashboard"""
    data = {
        'total_users': UserProfile.objects.count(),
        'total_buses': Bus.objects.count(),
        'active_registrations': BusRegistration.objects.filter(status='confirmed').count(),
        'pending_payments': BusRegistration.objects.filter(payment_status='pending').count(),
        'revenue_today': Payment.objects.filter(
            payment_date__date=datetime.now().date(),
            status='success'
        ).aggregate(total=models.Sum('amount'))['total'] or 0,
    }
    return JsonResponse(data)
