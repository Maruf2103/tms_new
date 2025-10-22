# custom_admin/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from transportation.models import *
from django.db.models import Count
from datetime import datetime, timedelta

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
    recent_registrations = BusRegistration.objects.select_related('user', 'bus').order_by('-registration_date')[:5]
    
    context = {
        'total_users': total_users,
        'total_buses': total_buses,
        'active_registrations': active_registrations,
        'pending_payments': pending_payments,
        'recent_registrations': recent_registrations,
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
    
    context = {
        'users': users,
    }
    return render(request, 'custom_admin/user_management.html', context)

@login_required
@user_passes_test(is_admin)
def admin_registration_management(request):
    """Registration Management View"""
    registrations = BusRegistration.objects.select_related('user', 'bus').all().order_by('-registration_date')
    
    context = {
        'registrations': registrations,
    }
    return render(request, 'custom_admin/registration_management.html', context)

@login_required
@user_passes_test(is_admin)
def admin_reports(request):
    """Reports and Analytics View"""
    # Basic statistics for demo
    user_distribution = UserProfile.objects.values('user_type').annotate(count=Count('id'))
    bus_utilization = Bus.objects.annotate(registration_count=Count('busregistration'))
    
    context = {
        'user_distribution': list(user_distribution),
        'bus_utilization': bus_utilization,
    }
    return render(request, 'custom_admin/reports.html', context)

@login_required
@user_passes_test(is_admin)
def admin_system_settings(request):
    """System Settings View"""
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
    }
    return JsonResponse(data)
