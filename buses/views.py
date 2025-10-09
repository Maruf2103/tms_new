from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Bus, Route, BusSchedule
from . import forms


@login_required
def bus_list(request):
    """Display list of all buses"""
    buses = Bus.objects.filter(status='active')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        buses = buses.filter(
            Q(bus_number__icontains=search_query) |
            Q(bus_name__icontains=search_query)
        )

    context = {
        'buses': buses,
        'search_query': search_query,
    }
    return render(request, 'buses/bus_list.html', context)


@login_required
def bus_detail(request, bus_id):
    """Display bus details and schedules"""
    bus = get_object_or_404(Bus, id=bus_id)
    schedules = BusSchedule.objects.filter(bus=bus, is_active=True)

    context = {
        'bus': bus,
        'schedules': schedules,
    }
    return render(request, 'buses/bus_detail.html', context)


@login_required
def route_list(request):
    """Display list of all routes"""
    routes = Route.objects.filter(is_active=True)

    context = {
        'routes': routes,
    }
    return render(request, 'buses/route_list.html', context)


@login_required
def schedule_list(request):
    """Display all bus schedules"""
    schedules = BusSchedule.objects.filter(is_active=True).select_related('bus', 'route')

    # Filter by shift
    shift = request.GET.get('shift', '')
    if shift:
        schedules = schedules.filter(shift=shift)

    # Filter by route
    route_id = request.GET.get('route', '')
    if route_id:
        schedules = schedules.filter(route_id=route_id)

    routes = Route.objects.filter(is_active=True)

    context = {
        'schedules': schedules,
        'routes': routes,
        'selected_shift': shift,
        'selected_route': route_id,
    }
    return render(request, 'buses/schedule_list.html', context)


# Authority Only Views
@login_required
def manage_buses(request):
    """Manage buses (Authority only)"""
    if request.user.user_type != 'authority':
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')

    buses = Bus.objects.all().order_by('-created_at')

    context = {
        'buses': buses,
    }
    return render(request, 'buses/manage_buses.html', context)


@login_required
def add_bus(request):
    """Add new bus (Authority only)"""
    if request.user.user_type != 'authority':
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = Bus(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bus added successfully!')
            return redirect('buses:manage_buses')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = Bus()

    return render(request, 'buses/bus_form.html', {'form': form, 'title': 'Add Bus'})


@login_required
def edit_bus(request, bus_id):
    """Edit bus (Authority only)"""
    if request.user.user_type != 'authority':
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')

    bus = get_object_or_404(Bus, id=bus_id)

    if request.method == 'POST':
        form = Bus(request.POST, request.FILES, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bus updated successfully!')
            return redirect('buses:manage_buses')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = Bus(instance=bus)

    return render(request, 'buses/bus_form.html', {'form': form, 'title': 'Edit Bus', 'bus': bus})


@login_required
def delete_bus(request, bus_id):
    """Delete bus (Authority only)"""
    if request.user.user_type != 'authority':
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')

    bus = get_object_or_404(Bus, id=bus_id)

    if request.method == 'POST':
        bus_number = bus.bus_number
        bus.delete()
        messages.success(request, f'Bus {bus_number} deleted successfully!')
        return redirect('buses:manage_buses')

    return render(request, 'buses/bus_confirm_delete.html', {'bus': bus})


@login_required
def add_schedule(request):
    """Add bus schedule (Authority only)"""
    if request.user.user_type != 'authority':
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = BusScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule added successfully!')
            return redirect('buses:manage_buses')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusScheduleForm()

    return render(request, 'buses/schedule_form.html', {'form': form, 'title': 'Add Schedule'})