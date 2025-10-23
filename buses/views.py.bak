from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bus, BusSchedule, Route, Registration
from django.db.models import Q


@login_required
def bus_registration_view(request):
    """Complete bus registration process"""
    # Check if user has complete profile
    if not request.user.first_name or not request.user.last_name:
        messages.warning(request, 'Please complete your profile first.')
        return redirect('complete_profile')

    routes = Route.objects.all()
    selected_route = None
    schedules = None

    if request.method == 'POST':
        route_id = request.POST.get('route')
        schedule_id = request.POST.get('schedule')

        if route_id:
            selected_route = Route.objects.get(id=route_id)
            schedules = BusSchedule.objects.filter(bus__route_name=selected_route.route_name)

        if schedule_id:
            schedule = BusSchedule.objects.get(id=schedule_id)
            # Check if already registered
            if Registration.objects.filter(user=request.user, bus_schedule=schedule).exists():
                messages.error(request, 'You are already registered for this bus schedule.')
            elif schedule.available_seats > 0:
                registration = Registration(user=request.user, bus_schedule=schedule)
                registration.save()
                messages.success(request, 'Successfully registered for the bus!')
                return redirect('payment', registration_id=registration.id)
            else:
                messages.error(request, 'No available seats for this schedule.')

    return render(request, 'bus/registration.html', {
        'routes': routes,
        'selected_route': selected_route,
        'schedules': schedules
    })


@login_required
def complete_profile_view(request):
    """Complete user profile before bus registration"""
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('bus_registration')

    return render(request, 'bus/complete_profile.html')


@login_required
def payment_view(request, registration_id):
    """Handle payment for bus registration"""
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)

    if request.method == 'POST':
        # Simulate payment processing
        registration.payment_status = True
        registration.payment_amount = 50.00  # Fixed amount for demo
        registration.save()

        # Update available seats
        schedule = registration.bus_schedule
        schedule.available_seats -= 1
        schedule.save()

        messages.success(request, 'Payment successful! Registration completed.')
        return redirect('my_registrations')

    return render(request, 'bus/payment.html', {'registration': registration})


@login_required
def view_schedules(request):
    """View all bus schedules"""
    schedules = BusSchedule.objects.all().select_related('bus')
    return render(request, 'bus/schedules.html', {'schedules': schedules})


@login_required
def view_routes(request):
    """View all bus routes"""
    routes = Route.objects.all()
    return render(request, 'bus/routes.html', {'routes': routes})


@login_required
def my_registrations_view(request):
    """View user's bus registrations"""
    registrations = Registration.objects.filter(user=request.user).select_related('bus_schedule__bus')
    return render(request, 'bus/my_registrations.html', {'registrations': registrations})


@login_required
def cancel_registration_view(request, registration_id):
    """Cancel a bus registration"""
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)

    if request.method == 'POST':
        # Restore available seat
        schedule = registration.bus_schedule
        schedule.available_seats += 1
        schedule.save()

        registration.delete()
        messages.success(request, 'Registration cancelled successfully.')
        return redirect('my_registrations')

    return render(request, 'bus/cancel_registration.html', {'registration': registration})


# Admin/Authority Views
@login_required
def manage_buses_view(request):
    """Manage buses (for transport authority)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    buses = Bus.objects.all()
    return render(request, 'bus/manage_buses.html', {'buses': buses})


@login_required
def add_bus_view(request):
    """Add new bus (for transport authority)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    if request.method == 'POST':
        bus_number = request.POST.get('bus_number')
        route_name = request.POST.get('route_name')
        capacity = request.POST.get('capacity')

        bus = Bus(bus_number=bus_number, route_name=route_name, capacity=capacity)
        bus.save()
        messages.success(request, 'Bus added successfully!')
        return redirect('manage_buses')

    return render(request, 'bus/add_bus.html')


@login_required
def edit_bus_view(request, bus_id):
    """Edit bus details (for transport authority)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    bus = get_object_or_404(Bus, id=bus_id)

    if request.method == 'POST':
        bus.bus_number = request.POST.get('bus_number')
        bus.route_name = request.POST.get('route_name')
        bus.capacity = request.POST.get('capacity')
        bus.save()
        messages.success(request, 'Bus updated successfully!')
        return redirect('manage_buses')

    return render(request, 'bus/edit_bus.html', {'bus': bus})


@login_required
def delete_bus_view(request, bus_id):
    """Delete bus (for transport authority)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    bus = get_object_or_404(Bus, id=bus_id)

    if request.method == 'POST':
        bus.delete()
        messages.success(request, 'Bus deleted successfully!')
        return redirect('manage_buses')

    return render(request, 'bus/delete_bus.html', {'bus': bus})


@login_required
def manage_schedules_view(request):
    """Manage bus schedules (for transport authority)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    schedules = BusSchedule.objects.all().select_related('bus')
    return render(request, 'bus/manage_schedules.html', {'schedules': schedules})


@login_required
def add_schedule_view(request):
    """Add new bus schedule (for transport authority)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    buses = Bus.objects.all()

    if request.method == 'POST':
        bus_id = request.POST.get('bus')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        available_seats = request.POST.get('available_seats')

        bus = Bus.objects.get(id=bus_id)
        schedule = BusSchedule(
            bus=bus,
            departure_time=departure_time,
            arrival_time=arrival_time,
            available_seats=available_seats
        )
        schedule.save()
        messages.success(request, 'Schedule added successfully!')
        return redirect('manage_schedules')

    return render(request, 'bus/add_schedule.html', {'buses': buses})


@login_required
def edit_schedule_view(request, schedule_id):
    """Edit bus schedule (for transport authority)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    schedule = get_object_or_404(BusSchedule, id=schedule_id)
    buses = Bus.objects.all()

    if request.method == 'POST':
        schedule.bus_id = request.POST.get('bus')
        schedule.departure_time = request.POST.get('departure_time')
        schedule.arrival_time = request.POST.get('arrival_time')
        schedule.available_seats = request.POST.get('available_seats')
        schedule.save()
        messages.success(request, 'Schedule updated successfully!')
        return redirect('manage_schedules')

    return render(request, 'bus/edit_schedule.html', {'schedule': schedule, 'buses': buses})