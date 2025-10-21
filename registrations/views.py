from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import BusRegistration, Payment, RegistrationHistory
from .forms import BusRegistrationForm, PaymentForm, SearchBusForm
from buses.models import BusSchedule, Route
from datetime import date


@login_required
def register_bus(request):
    """Register for a bus"""
    # Check if profile is complete
    if not request.user.profile.is_profile_complete:
        messages.warning(request, 'Please complete your profile first.')
        return redirect('accounts:complete_profile')

    # Search form
    search_form = SearchBusForm(request.GET or None)
    schedules = BusSchedule.objects.filter(is_active=True).select_related('bus', 'route')

    # Apply filters
    if search_form.is_valid():
        route = search_form.cleaned_data.get('route')
        shift = search_form.cleaned_data.get('shift')

        if route:
            schedules = schedules.filter(route=route)
        if shift:
            schedules = schedules.filter(shift=shift)

    context = {
        'search_form': search_form,
        'schedules': schedules,
    }
    return render(request, 'registrations/register_bus.html', context)


@login_required
def confirm_registration(request, schedule_id):
    """Confirm bus registration"""
    schedule = get_object_or_404(BusSchedule, id=schedule_id, is_active=True)

    # Check if user already has active registration for this schedule
    existing_registration = BusRegistration.objects.filter(
        user=request.user,
        bus_schedule=schedule,
        status='active'
    ).first()

    if existing_registration:
        messages.warning(request, 'You already have an active registration for this bus schedule.')
        return redirect('registrations:my_registrations')

    # Check available seats
    if schedule.available_seats() <= 0:
        messages.error(request, 'Sorry, no seats available for this schedule.')
        return redirect('registrations:register_bus')

    if request.method == 'POST':
        form = BusRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                registration = form.save(commit=False)
                registration.user = request.user
                registration.bus_schedule = schedule
                registration.save()

                # Create history entry
                RegistrationHistory.objects.create(
                    registration=registration,
                    action='CREATED',
                    description='Registration created',
                    performed_by=request.user
                )

                messages.success(request, 'Registration created! Please proceed to payment.')
                return redirect('registrations:payment', registration_id=registration.registration_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusRegistrationForm()

    context = {
        'form': form,
        'schedule': schedule,
    }
    return render(request, 'registrations/confirm_registration.html', context)


@login_required
def payment(request, registration_id):
    """Process payment for registration"""
    registration = get_object_or_404(BusRegistration, registration_id=registration_id, user=request.user)

    # Check if payment already exists
    if hasattr(registration, 'payment'):
        messages.info(request, 'Payment already processed for this registration.')
        return redirect('registrations:registration_detail', registration_id=registration_id)

    # Calculate amount (example: 500 BDT per month)
    days_difference = (registration.valid_until - registration.valid_from).days
    amount = (days_difference / 30) * 500

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                payment = form.save(commit=False)
                payment.registration = registration
                payment.amount = amount
                payment.save()

                # Update registration status
                registration.payment_status = 'paid'
                registration.status = 'active'
                registration.save()

                # Create history entry
                RegistrationHistory.objects.create(
                    registration=registration,
                    action='PAYMENT_COMPLETED',
                    description=f'Payment of {amount} BDT completed via {payment.payment_method}',
                    performed_by=request.user
                )

                messages.success(request, 'Payment successful! Your registration is now active.')
                return redirect('registrations:registration_detail', registration_id=registration_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PaymentForm(initial={'amount': amount})

    context = {
        'form': form,
        'registration': registration,
        'amount': amount,
    }
    return render(request, 'registrations/payment.html', context)


@login_required
def my_registrations(request):
    """View user's registrations"""
    registrations = BusRegistration.objects.filter(user=request.user).select_related(
        'bus_schedule__bus', 'bus_schedule__route'
    ).order_by('-created_at')

    context = {
        'registrations': registrations,
    }
    return render(request, 'registrations/my_registrations.html', context)


@login_required
def registration_detail(request, registration_id):
    """View registration details"""
    registration = get_object_or_404(
        BusRegistration,
        registration_id=registration_id,
        user=request.user
    )

    history = registration.history.all()

    context = {
        'registration': registration,
        'history': history,
    }
    return render(request, 'registrations/registration_detail.html', context)


@login_required
def cancel_registration(request, registration_id):
    """Cancel registration"""
    registration = get_object_or_404(BusRegistration, registration_id=registration_id, user=request.user)

    if registration.status == 'cancelled':
        messages.warning(request, 'This registration is already cancelled.')
        return redirect('registrations:my_registrations')

    if request.method == 'POST':
        with transaction.atomic():
            registration.status = 'cancelled'
            registration.save()

            # Create history entry
            RegistrationHistory.objects.create(
                registration=registration,
                action='CANCELLED',
                description='Registration cancelled by user',
                performed_by=request.user
            )

            messages.success(request, 'Registration cancelled successfully.')
            return redirect('registrations:my_registrations')

    return render(request, 'registrations/cancel_registration.html', {'registration': registration})


# Authority Views
@login_required
def all_registrations(request):
    """View all registrations (Authority only)"""
    if request.user.user_type != 'authority':
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')

    registrations = BusRegistration.objects.all().select_related(
        'user', 'bus_schedule__bus', 'bus_schedule__route'
    ).order_by('-created_at')

    # Filter by status
    status = request.GET.get('status', '')
    if status:
        registrations = registrations.filter(status=status)

    context = {
        'registrations': registrations,
        'selected_status': status,
    }
    return render(request, 'registrations/all_registrations.html', context)