from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import BusLocation, BusStatus, Notification
from .forms import BusLocationForm, BusStatusForm, NotificationForm
from buses.models import Bus




@login_required
def live_tracking(request):
    """Display live tracking map"""
    buses = Bus.objects.filter(status='active')
    
    # Get latest location for each bus
    bus_locations = []
    for bus in buses:
        try:
            location = BusLocation.objects.filter(bus=bus, is_active=True).latest()
            bus_locations.append({
                'bus': bus,
                'location': location,
                'status': getattr(bus, 'current_status', None)
            })
        except BusLocation.DoesNotExist:
            pass
    
    context = {
        'bus_locations': bus_locations,
    }
    return render(request, 'tracking/live_tracking.html', context)

@login_required
def bus_tracking_detail(request, bus_id):
    """Display detailed tracking for a specific bus"""
    bus = get_object_or_404(Bus, id=bus_id)
    
    try:
        current_location = BusLocation.objects.filter(bus=bus, is_active=True).latest()
    except BusLocation.DoesNotExist:
        current_location = None
    
    try:
        bus_status = bus.current_status
    except BusStatus.DoesNotExist:
        bus_status = None
    
    notifications = Notification.objects.filter(bus=bus, is_active=True).order_by('-created_at')[:5]
    location_history = BusLocation.objects.filter(bus=bus).order_by('-timestamp')[:20]
    
    context = {
        'bus': bus,
        'current_location': current_location,
        'bus_status': bus_status,
        'notifications': notifications,
        'location_history': location_history,
    }
    return render(request, 'tracking/bus_tracking_detail.html', context)

@login_required
def get_bus_location_api(request, bus_id):
    """API endpoint to get bus location (for AJAX updates)"""
    bus = get_object_or_404(Bus, id=bus_id)
    
    try:
        location = BusLocation.objects.filter(bus=bus, is_active=True).latest()
        data = {
            'success': True,
            'latitude': float(location.latitude),
            'longitude': float(location.longitude),
            'speed': float(location.speed) if location.speed else 0,
            'heading': float(location.heading) if location.heading else 0,
            'timestamp': location.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
    except BusLocation.DoesNotExist:
        data = {
            'success': False,
            'message': 'Location not available'
        }
    
    return JsonResponse(data)

# Authority Views
@login_required
def manage_tracking(request):
    """Manage tracking (Authority only)"""
    # allow either a bus_user_profile with user_type authority/admin or any staff user
    profile = getattr(request.user, 'bus_user_profile', None)
    if not ((profile and profile.user_type in ('authority', 'admin')) or request.user.is_staff):
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')
    
    buses = Bus.objects.filter(status='active')
    bus_statuses = BusStatus.objects.all()
    recent_locations = BusLocation.objects.filter(is_active=True).select_related('bus')[:20]
    
    context = {
        'buses': buses,
        'bus_statuses': bus_statuses,
        'recent_locations': recent_locations,
    }
    return render(request, 'tracking/manage_tracking.html', context)

@login_required
def update_location(request):
    """Update bus location (Authority only)"""
    profile = getattr(request.user, 'bus_user_profile', None)
    if not ((profile and profile.user_type in ('authority', 'admin')) or request.user.is_staff):
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = BusLocationForm(request.POST)
        if form.is_valid():
            # Deactivate previous locations for this bus
            bus = form.cleaned_data['bus']
            BusLocation.objects.filter(bus=bus).update(is_active=False)
            
            # Save new location
            form.save()
            messages.success(request, 'Location updated successfully!')
            return redirect('tracking:manage_tracking')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusLocationForm()
    
    return render(request, 'tracking/location_form.html', {'form': form, 'title': 'Update Location'})

@login_required
def update_status(request, bus_id=None):
    """Update bus status (Authority only)"""
    profile = getattr(request.user, 'bus_user_profile', None)
    if not ((profile and profile.user_type in ('authority', 'admin')) or request.user.is_staff):
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')
    
    if bus_id:
        bus = get_object_or_404(Bus, id=bus_id)
        bus_status, created = BusStatus.objects.get_or_create(bus=bus)
    else:
        bus_status = None
    
    if request.method == 'POST':
        form = BusStatusForm(request.POST, instance=bus_status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bus status updated successfully!')
            return redirect('tracking:manage_tracking')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusStatusForm(instance=bus_status)
    
    return render(request, 'tracking/status_form.html', {'form': form, 'title': 'Update Status'})

@login_required
def create_notification(request):
    """Create notification (Authority only)"""
    profile = getattr(request.user, 'bus_user_profile', None)
    if not ((profile and profile.user_type in ('authority', 'admin')) or request.user.is_staff):
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification created successfully!')
            return redirect('tracking:manage_tracking')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NotificationForm()
    
    return render(request, 'tracking/notification_form.html', {'form': form, 'title': 'Create Notification'})

@login_required
def notifications_list(request):
    """View all notifications"""
    notifications = Notification.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'notifications': notifications,
    }

    return render(request, 'tracking/notifications_list.html', context)




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Vehicle
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json


@method_decorator(csrf_exempt, name='dispatch')
class UpdateLocationView(View):
    def post(self, request):
        vehicle_id = request.POST.get('vehicle_id')
        lat = float(request.POST.get('latitude'))
        lng = float(request.POST.get('longitude'))

        vehicle, created = Vehicle.objects.update_or_create(
            vehicle_id=vehicle_id,
            defaults={'latitude': lat, 'longitude': lng}
        )

        # Broadcast update to WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "tracking",
            {
                "type": "send_location_update",
                "data": {
                    "vehicle_id": vehicle.vehicle_id,
                    "name": vehicle.name,
                    "latitude": lat,
                    "longitude": lng,
                }
            }
        )
        return JsonResponse({"status": "success"})

from django.shortcuts import render

def live_map(request):
    return render(request, 'tracking/live_map.html')
