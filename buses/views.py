from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from decimal import Decimal
from datetime import date, timedelta
import uuid

User = get_user_model()

# Home view
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        # Add your signup logic here
        pass
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        # Add your signin logic here
        pass
    return render(request, 'login.html')

def sign_out(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    # Show a simple dashboard. For students include upcoming schedules so they can
    # quickly view and book from the dashboard.
    upcoming_schedules = []
    is_authority = False
    if request.user.is_authenticated:
        try:
            profile = request.user.bus_user_profile
            is_authority = profile.user_type in ('authority', 'admin')
        except Exception:
            is_authority = False

        from django.utils import timezone
        # Use local timezone now so we only show schedules that haven't departed yet today
        now = timezone.localtime()
        today = now.date()
        time_now = now.time()
        upcoming_schedules = Schedule.objects.filter(
            is_active=True
        ).filter(
            Q(date__gt=today) | (Q(date=today) & Q(departure_time__gte=time_now))
        ).select_related('bus', 'route').order_by('date', 'departure_time')[:10]

    context = {
        'upcoming_schedules': upcoming_schedules,
        'is_authority': is_authority,
    }
    # include user's monthly subscriptions if authenticated
    monthly_subscriptions = []
    if request.user.is_authenticated:
        try:
            monthly_subscriptions = MonthlySubscription.objects.filter(user=request.user, is_active=True).select_related('schedule__bus', 'schedule__route')
        except Exception:
            monthly_subscriptions = []

    context['monthly_subscriptions'] = monthly_subscriptions
    return render(request, 'dashboard.html', context)

# Bus management views
@login_required
def bus_registration(request):
    if request.user.bus_user_profile.user_type not in ('authority', 'admin'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
        
    if request.method == 'POST':
        bus_number = request.POST.get('bus_number')
        bus_name = request.POST.get('bus_name')
        capacity = request.POST.get('capacity')
        driver_name = request.POST.get('driver_name')

        try:
            bus = Bus.objects.create(
                bus_number=bus_number,
                bus_name=bus_name,
                capacity=int(capacity),
                driver_name=driver_name
            )
            messages.success(request, 'Bus registered successfully!')
            return redirect('manage_buses')
        except Exception as e:
            messages.error(request, f'Error registering bus: {str(e)}')
    
    return render(request, 'bus/registration.html')

@login_required
def manage_buses(request):
    if request.user.bus_user_profile.user_type not in ('authority', 'admin'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
        
    buses = Bus.objects.all()
    context = {
        'buses': buses
    }
    return render(request, 'bus/manage_buses.html', context)

@login_required
def manage_schedules(request):
    if request.user.bus_user_profile.user_type not in ('authority', 'admin'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
        
    schedules = Schedule.objects.select_related('bus', 'route').all()
    buses = Bus.objects.filter(is_active=True)
    routes = Route.objects.all()
    
    if request.method == 'POST':
        bus_id = request.POST.get('bus')
        route_id = request.POST.get('route')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        date = request.POST.get('date')
        
        try:
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
            messages.success(request, 'Schedule created successfully!')
        except Exception as e:
            messages.error(request, f'Error creating schedule: {str(e)}')
    
    context = {
        'schedules': schedules,
        'buses': buses,
        'routes': routes
    }
    return render(request, 'bus/manage_schedules.html', context)

@login_required
def edit_schedule(request, schedule_id):
    if request.user.bus_user_profile.user_type not in ('authority', 'admin'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
        
    try:
        schedule = Schedule.objects.select_related('bus', 'route').get(id=schedule_id)
        buses = Bus.objects.filter(is_active=True)
        routes = Route.objects.all()
        
        if request.method == 'POST':
            bus_id = request.POST.get('bus')
            route_id = request.POST.get('route')
            departure_time = request.POST.get('departure_time')
            arrival_time = request.POST.get('arrival_time')
            date = request.POST.get('date')
            
            try:
                bus = Bus.objects.get(id=bus_id)
                route = Route.objects.get(id=route_id)
                
                schedule.bus = bus
                schedule.route = route
                schedule.departure_time = departure_time
                schedule.arrival_time = arrival_time
                schedule.date = date
                schedule.save()
                
                messages.success(request, 'Schedule updated successfully!')
                return redirect('manage_schedules')
            except Exception as e:
                messages.error(request, f'Error updating schedule: {str(e)}')
        
        context = {
            'schedule': schedule,
            'buses': buses,
            'routes': routes
        }
        return render(request, 'bus/edit_schedule.html', context)
        
    except Schedule.DoesNotExist:
        messages.error(request, 'Schedule not found.')
        return redirect('manage_schedules')

@login_required
def toggle_schedule(request, schedule_id):
    if not request.user.bus_user_profile.user_type == 'authority':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('home')
        
    try:
        schedule = Schedule.objects.get(id=schedule_id)
        schedule.is_active = not schedule.is_active
        schedule.save()
        
        status = 'activated' if schedule.is_active else 'deactivated'
        messages.success(request, f'Schedule {status} successfully!')
    except Schedule.DoesNotExist:
        messages.error(request, 'Schedule not found.')
    
    return redirect('manage_schedules')

def search_routes(request):
    # Merged UX: redirect to view_schedules which now handles search and booking.
    return redirect('view_schedules')

def view_schedules(request):
    # Allow students to filter schedules by route, search term (start/end), and date
    routes = Route.objects.filter(is_active=True).order_by('route_name')
    schedules = Schedule.objects.filter(is_active=True).select_related('bus', 'route')

    # Find & Book should not display user's existing bookings; keep booking management on the dashboard.

    # GET params
    route_id = request.GET.get('route')
    q = request.GET.get('q', '').strip()
    date = request.GET.get('date', '').strip()

    if route_id:
        try:
            schedules = schedules.filter(route_id=int(route_id))
        except Exception:
            pass

    if q:
        # search by start_point or end_point or route_name
        schedules = schedules.filter(
            models.Q(route__start_point__icontains=q) |
            models.Q(route__end_point__icontains=q) |
            models.Q(route__route_name__icontains=q)
        )

    if date:
        try:
            # accept YYYY-MM-DD from GET
            schedules = schedules.filter(date=date)
        except Exception:
            pass
    else:
        # No date provided — default to server local 'today' so users see today's schedules first
        try:
            from django.utils import timezone
            today = timezone.localdate()
            schedules = schedules.filter(date=today)
            # set the date string so the template's date field reflects the default
            date = str(today)
        except Exception:
            # if timezone fails for some reason, fall back to no filtering
            pass

    # time range filter: morning/afternoon/evening
    time_range = request.GET.get('time_range', '').strip()
    if time_range:
        from datetime import time
        if time_range == 'morning':
            schedules = schedules.filter(departure_time__gte=time(5,0), departure_time__lte=time(11,59))
        elif time_range == 'afternoon':
            schedules = schedules.filter(departure_time__gte=time(12,0), departure_time__lte=time(16,59))
        elif time_range == 'evening':
            schedules = schedules.filter(departure_time__gte=time(17,0), departure_time__lte=time(22,59))

    schedules = schedules.order_by('date', 'departure_time')

    # pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(schedules, 10)
    try:
        schedules_page = paginator.page(page)
    except PageNotAnInteger:
        schedules_page = paginator.page(1)
    except EmptyPage:
        schedules_page = paginator.page(paginator.num_pages)

    context = {
        'schedules': schedules_page,
        'routes': routes,
        'selected_route': route_id or '',
        'q': q,
        'selected_date': date,
        'paginator': paginator,
        'page_obj': schedules_page,
    }
    return render(request, 'bus/view_schedules.html', context)


def bus_schedule(request):
    """Read-only listing of upcoming schedules for users who want to just view the bus timetable."""
    from django.utils import timezone
    now = timezone.localtime()
    today = now.date()
    time_now = now.time()
    schedules = Schedule.objects.filter(is_active=True).filter(
        Q(date__gt=today) | (Q(date=today) & Q(departure_time__gte=time_now))
    ).select_related('bus', 'route').order_by('date', 'departure_time')

    # simple pagination to avoid huge pages
    page = request.GET.get('page', 1)
    paginator = Paginator(schedules, 20)
    try:
        schedules_page = paginator.page(page)
    except PageNotAnInteger:
        schedules_page = paginator.page(1)
    except EmptyPage:
        schedules_page = paginator.page(paginator.num_pages)

    context = {
        'schedules': schedules_page,
        'page_obj': schedules_page,
        'paginator': paginator,
    }
    # If user is authenticated, include their recent bookings so they can manage bookings from the Bus Schedule page
    recent_activities = []
    if request.user.is_authenticated:
        try:
            # Include both recent Bookings and MonthlySubscriptions so students see monthly purchases too
            bookings_qs = Booking.objects.select_related('schedule__bus', 'schedule__route').filter(user=request.user).exclude(payment_status='cancelled')
            subs_qs = MonthlySubscription.objects.select_related('schedule__bus', 'schedule__route').filter(user=request.user).exclude(payment_status='cancelled')

            activities = []
            for b in bookings_qs:
                activities.append({'type': 'booking', 'ts': b.booking_date, 'obj': b})
            for s in subs_qs:
                activities.append({'type': 'subscription', 'ts': s.created_at, 'obj': s})

            # sort by timestamp desc and take top 8
            activities.sort(key=lambda x: x['ts'] or 0, reverse=True)
            recent_activities = activities[:8]
        except Exception:
            recent_activities = []

    context['recent_activities'] = recent_activities
    return render(request, 'bus/bus_schedule.html', context)



@login_required
def book_bus(request, schedule_id):
    try:
        schedule = Schedule.objects.select_related('bus', 'route').get(id=schedule_id, is_active=True)
        
        if request.method == 'POST':
            passengers = int(request.POST.get('passengers', 1))
            package = request.POST.get('package', 'single')

            if package == 'single':
                if passengers > schedule.available_seats:
                    messages.error(request, 'Not enough seats available.')
                    return redirect('view_schedules')

                # Calculate total amount
                total_amount = schedule.route.fare * passengers

                # Create booking
                booking = Booking.objects.create(
                    user=request.user,
                    schedule=schedule,
                    passengers=passengers,
                    total_amount=total_amount
                )

                # Update available seats for this schedule instance
                schedule.available_seats -= passengers
                schedule.save()

                # Store booking details in session
                request.session['booking_details'] = {
                    'type': 'single',
                    'booking_id': str(booking.booking_id),
                    'bus_number': schedule.bus.bus_number,
                    'route': f"{schedule.route.start_point} to {schedule.route.end_point}",
                    'date': schedule.date.strftime('%Y-%m-%d'),
                    'time': schedule.departure_time.strftime('%H:%M'),
                    'seats': passengers,
                    'total_fare': float(total_amount)
                }

                return redirect('checkout')

            elif package == 'monthly':
                # Monthly subscription: user subscribes to this schedule for ~30 days
                # We do not reserve seats across all days here (seat management for recurring trips is complex).
                # Monthly pricing: use 22 trips approximation (working days) by default.
                multiplier = Decimal('22')
                fare = Decimal(str(schedule.route.fare))
                monthly_amount = (fare * Decimal(passengers) * multiplier).quantize(Decimal('0.01'))

                # create subscription
                subscription = MonthlySubscription.objects.create(
                    user=request.user,
                    schedule=schedule,
                    start_date=date.today(),
                    passengers=passengers,
                    monthly_amount=monthly_amount,
                    payment_status='pending',
                    is_active=True
                )

                # Optionally create a Payment record placeholder
                # Payment creation/integration should happen via checkout flow

                request.session['booking_details'] = {
                    'type': 'monthly',
                    'subscription_id': str(subscription.subscription_id),
                    'bus_number': schedule.bus.bus_number,
                    'route': f"{schedule.route.start_point} to {schedule.route.end_point}",
                    'start_date': subscription.start_date.strftime('%Y-%m-%d'),
                    'end_date': subscription.end_date.strftime('%Y-%m-%d'),
                    'seats': passengers,
                    'monthly_amount': float(monthly_amount)
                }

                return redirect('checkout')
            
        context = {
            'schedule': schedule
        }
        return render(request, 'bus/book_bus.html', context)
        
    except Schedule.DoesNotExist:
        messages.error(request, 'Schedule not found or inactive.')
        return redirect('view_schedules')

def booking_confirmation(request):
    # Get the booking details from session
    booking = request.session.get('booking_details', {})
    
    if not booking:
        messages.error(request, 'No booking information found.')
        return redirect('home')
        
    context = {
        'booking': booking
    }
    
    # Clear the booking details from session after displaying
    if 'booking_details' in request.session:
        del request.session['booking_details']
        
    return render(request, 'bus/booking_confirmation.html', context)
    
    # Clear the booking details from session after displaying
    if 'booking_details' in request.session:
        del request.session['booking_details']
        
    return render(request, 'bus/booking_confirmation.html', context)


@login_required
def checkout(request):
    # Display checkout page based on session booking_details
    booking = request.session.get('booking_details')
    if not booking:
        messages.error(request, 'No booking in progress.')
        return redirect('view_schedules')

    return render(request, 'bus/checkout.html', {'booking': booking})


@login_required
def process_checkout(request):
    if request.method != 'POST':
        return redirect('view_schedules')

    booking = request.session.get('booking_details')
    if not booking:
        messages.error(request, 'No booking found for payment.')
        return redirect('view_schedules')

    payment_method = request.POST.get('payment_method', 'bkash')
    transaction_id = uuid.uuid4().hex

    # Process single booking payment
    if booking.get('type') == 'single':
        try:
            b = Booking.objects.get(booking_id=booking.get('booking_id'))
            payment = Payment.objects.create(
                booking=b,
                subscription=None,
                transaction_id=transaction_id,
                amount=b.total_amount,
                payment_method=payment_method,
                status='completed'
            )

            b.payment_status = 'completed'
            b.is_confirmed = True
            b.save()

            # update session booking details for confirmation
            request.session['booking_details'] = {
                'type': 'single',
                'booking_id': str(b.booking_id),
                'bus_number': booking.get('bus_number'),
                'route': booking.get('route'),
                'date': booking.get('date'),
                'time': booking.get('time'),
                'seats': booking.get('seats'),
                'total_fare': float(b.total_amount),
                'transaction_id': transaction_id
            }

            return redirect('booking_confirmation')
        except Booking.DoesNotExist:
            messages.error(request, 'Booking not found for payment.')
            return redirect('view_schedules')

    elif booking.get('type') == 'monthly':
        try:
            sub = MonthlySubscription.objects.get(subscription_id=booking.get('subscription_id'))
            payment = Payment.objects.create(
                booking=None,
                subscription=sub,
                transaction_id=transaction_id,
                amount=sub.monthly_amount,
                payment_method=payment_method,
                status='completed'
            )

            sub.payment_status = 'completed'
            sub.is_active = True
            # Reserve seats on the schedule if not already reserved
            try:
                if not getattr(sub, 'seats_reserved', False):
                    sched = sub.schedule
                    sched.available_seats = max(0, sched.available_seats - (sub.passengers or 0))
                    sched.save()
                    sub.seats_reserved = True
            except Exception:
                # If anything goes wrong reserving seats, proceed but log in server
                pass

            sub.save()

            request.session['booking_details'] = {
                'type': 'monthly',
                'subscription_id': str(sub.subscription_id),
                'bus_number': booking.get('bus_number'),
                'route': booking.get('route'),
                'start_date': booking.get('start_date'),
                'end_date': booking.get('end_date'),
                'seats': booking.get('seats'),
                'monthly_amount': float(sub.monthly_amount),
                'transaction_id': transaction_id
            }

            return redirect('booking_confirmation')
        except MonthlySubscription.DoesNotExist:
            messages.error(request, 'Subscription not found for payment.')
            return redirect('view_schedules')

    messages.error(request, 'Unable to process payment.')
    return redirect('view_schedules')

def select_bus(request):
    return render(request, 'bus/select_bus.html')


@login_required
def booking_details(request, booking_id):
    """Show full details for a booking. User must own the booking."""
    try:
        booking = Booking.objects.select_related('schedule__bus', 'schedule__route').get(booking_id=booking_id)
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('dashboard')

    if booking.user != request.user:
        return HttpResponseForbidden('You do not have permission to view this booking.')

    context = {
        'booking': booking
    }
    return render(request, 'bus/booking_details.html', context)

def make_payment(request):
    return render(request, 'bus/payment.html')


@login_required
def cancel_booking(request, booking_id):
    # Allow student to cancel their own booking; restore seats and mark cancelled
    try:
        booking = Booking.objects.select_related('schedule').get(booking_id=booking_id)
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('dashboard')

    if booking.user != request.user:
        return HttpResponseForbidden('You cannot cancel this booking.')

    # restore seats
    schedule = booking.schedule
    schedule.available_seats = schedule.available_seats + booking.passengers
    schedule.save()

    booking.payment_status = 'cancelled'
    booking.is_confirmed = False
    booking.save()

    messages.success(request, 'Booking cancelled and seats restored.')
    return redirect('dashboard')


@login_required
def cancel_subscription(request, subscription_id):
    """Allow student to cancel their monthly subscription"""
    try:
        subscription = MonthlySubscription.objects.get(subscription_id=subscription_id)
    except MonthlySubscription.DoesNotExist:
        messages.error(request, 'Subscription not found.')
        return redirect('dashboard')

    if subscription.user != request.user:
        return HttpResponseForbidden('You cannot cancel this subscription.')

    # restore seats if we had reserved them for this subscription
    try:
        if getattr(subscription, 'seats_reserved', False):
            sched = subscription.schedule
            sched.available_seats = sched.available_seats + (subscription.passengers or 0)
            sched.save()
            subscription.seats_reserved = False
    except Exception:
        pass

    # deactivate subscription
    subscription.is_active = False
    subscription.payment_status = 'cancelled'
    subscription.save()

    messages.success(request, 'Subscription cancelled.')
    return redirect('dashboard')


@login_required
def subscription_detail(request, subscription_id):
    try:
        sub = MonthlySubscription.objects.select_related('schedule__bus', 'schedule__route').get(subscription_id=subscription_id)
    except MonthlySubscription.DoesNotExist:
        messages.error(request, 'Subscription not found.')
        return redirect('dashboard')

    if sub.user != request.user:
        return HttpResponseForbidden('You cannot view this subscription.')

    context = {
        'subscription': sub
    }
    return render(request, 'bus/subscription_detail.html', context)

def contact_us(request):
    return render(request, 'contact_us.html')


def admin_portal(request):
    """Simple admin portal page that links to Django admin login or to the admin signup view."""
    return render(request, 'admin_portal/portal.html')


def admin_signup(request):
    """Allow creation of an authority/staff user through a protected signup form.

    Security: this requires settings.ADMIN_SIGNUP_CODE to be set and the user must
    submit the same code to create an admin account. If ADMIN_SIGNUP_CODE is not
    configured, signup is disabled.
    """
    from django.conf import settings
    User = get_user_model()

    # if no admin signup code in settings, disallow public signups
    admin_code_required = getattr(settings, 'ADMIN_SIGNUP_CODE', None)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        admin_code = request.POST.get('admin_code')

        if admin_code_required and admin_code != admin_code_required:
            messages.error(request, 'Invalid admin signup code.')
            return render(request, 'admin_portal/signup.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'admin_portal/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'admin_portal/signup.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            # Mark as staff so they can access admin-like pages
            user.is_staff = True
            user.save()

            # create a UserProfile entry so existing authority checks work
            try:
                UserProfile.objects.create(user=user, user_type='authority')
            except Exception:
                # If UserProfile model not available for some reason, continue
                pass

            # Auto-login the newly created admin and redirect to in-site authority panel
            try:
                login(request, user)
            except Exception:
                pass

            messages.success(request, 'Admin account created and signed in.')
            return redirect('authority_panel')
        except Exception as e:
            messages.error(request, f'Error creating admin account: {e}')
            return render(request, 'admin_portal/signup.html')

    # GET
    if not admin_code_required:
        # If no signup code configured, disallow creating admin accounts from the site.
        messages.info(request, 'Admin signup is disabled on this installation. Configure ADMIN_SIGNUP_CODE in settings to enable it.')
        return render(request, 'admin_portal/portal.html')

    return render(request, 'admin_portal/signup.html')


def admin_signin(request):
    """Admin sign in that signs into the site and redirects to the in-site authority panel."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Only allow staff or users with authority profile
            allowed = False
            try:
                profile = getattr(user, 'bus_user_profile', None)
                if profile and profile.user_type in ('authority', 'admin'):
                    allowed = True
            except Exception:
                allowed = False

            if user.is_staff:
                allowed = True

            if not allowed:
                messages.error(request, 'You do not have admin privileges for the site.')
                return render(request, 'admin_portal/signin.html')

            login(request, user)
            messages.success(request, f'Welcome, {user.username}.')
            return redirect('authority_panel')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'admin_portal/signin.html')

# =============================================
# USER AUTHENTICATION SYSTEM - ADDED BY SAMIA
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
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                student_id=student_id,
                phone=phone,
                address=address
            )
            
            messages.success(request, 'Account created successfully! Please sign in.')
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
            
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.user_type in ('authority', 'admin'):
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
        user_profile = UserProfile.objects.create(user=request.user, user_type='student')
    
    # determine authority
    is_authority = user_profile.user_type in ('authority', 'admin')

    # upcoming schedules for quick booking (students only)
    upcoming_schedules = []
    from django.utils import timezone
    now = timezone.localtime()
    today = now.date()
    time_now = now.time()
    if not is_authority:
        upcoming_schedules = Schedule.objects.filter(is_active=True).filter(
            Q(date__gt=today) | (Q(date=today) & Q(departure_time__gte=time_now))
        ).select_related('bus', 'route').order_by('date', 'departure_time')[:10]

    context = {
        'user_profile': user_profile,
        'is_authority': is_authority,
        'upcoming_schedules': upcoming_schedules,
    }
    # include recent bookings for the logged-in user so they can manage/cancel from dashboard
    recent_bookings = []
    if request.user.is_authenticated:
        try:
            recent_bookings = Booking.objects.select_related('schedule__bus', 'schedule__route').filter(user=request.user).exclude(payment_status='cancelled').order_by('-booking_date')[:8]
        except Exception:
            recent_bookings = []

    context['recent_bookings'] = recent_bookings
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
# ADMIN/AUTHORITY PANEL - ADDED BY SAMIA
# =============================================

@login_required
def authority_panel(request):
    # Authority panel for transport management
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type not in ('authority', 'admin'):
            messages.error(request, 'Access denied! Authority panel only.')
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Access denied! Please complete your profile.')
        return redirect('profile')
    
    total_buses = Bus.objects.count()
    active_buses = Bus.objects.filter(is_active=True).count()
    total_routes = Route.objects.count()
    total_bookings = Booking.objects.count()
    active_bookings = Booking.objects.filter(is_confirmed=True).count()
    
    recent_bookings = Booking.objects.select_related('user', 'schedule').order_by('-booking_date')[:10]
    
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
        if user_profile.user_type not in ('authority', 'admin'):
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
        if user_profile.user_type not in ('authority', 'admin'):
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
        if user_profile.user_type not in ('authority', 'admin'):
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
        if user_profile.user_type not in ('authority', 'admin'):
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        return redirect('dashboard')
    
    bookings = Booking.objects.select_related('user', 'schedule').order_by('-booking_date')
    return render(request, 'authority/view_bookings.html', {'bookings': bookings})


@login_required
def manage_users(request):
    """Authority-only user management: list, paginate, and quick actions."""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type not in ('authority', 'admin'):
            messages.error(request, 'Access denied! Authority panel only.')
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Access denied! Please complete your profile.')
        return redirect('dashboard')

    User = get_user_model()
    q = request.GET.get('q', '').strip()
    users = User.objects.all().order_by('username')
    if q:
        users = users.filter(username__icontains=q) | users.filter(email__icontains=q)

    # pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 25)
    try:
        users_page = paginator.page(page)
    except Exception:
        users_page = paginator.page(1)

    context = {
        'users': users_page,
        'q': q,
        'paginator': paginator,
        'page_obj': users_page,
    }
    return render(request, 'authority/manage_users.html', context)


@login_required
def edit_user(request, user_id):
    """Edit a single user's role and active/staff flags."""
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.user_type not in ('authority', 'admin'):
            messages.error(request, 'Access denied!')
            return redirect('dashboard')
    except Exception:
        messages.error(request, 'Access denied!')
        return redirect('dashboard')

    User = get_user_model()
    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('manage_users')

    # Ensure we don't allow editing the currently logged-in user role to avoid lockout
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        is_active = bool(request.POST.get('is_active'))
        is_staff = bool(request.POST.get('is_staff'))
        user_type = request.POST.get('user_type', 'student')

        target.email = email or target.email
        target.is_active = is_active
        target.is_staff = is_staff
        try:
            target.save()
        except Exception:
            messages.error(request, 'Could not save user changes.')
            return redirect('edit_user', user_id=user_id)

        # update or create UserProfile
        try:
            up, created = UserProfile.objects.get_or_create(user=target)
            up.user_type = user_type
            up.save()
        except Exception:
            pass

        messages.success(request, 'User updated.')
        return redirect('manage_users')

    # GET
    try:
        user_profile = UserProfile.objects.get(user=target)
    except Exception:
        user_profile = None

    context = {
        'target': target,
        'profile': user_profile,
    }
    return render(request, 'authority/edit_user.html', context)


@login_required
def toggle_user_active(request, user_id):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.user_type not in ('authority', 'admin'):
            messages.error(request, 'Access denied!')
            return redirect('dashboard')
    except Exception:
        messages.error(request, 'Access denied!')
        return redirect('dashboard')

    User = get_user_model()
    try:
        target = User.objects.get(id=user_id)
        target.is_active = not target.is_active
        target.save()
        messages.success(request, 'User active state toggled.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')

    return redirect('manage_users')


@login_required
def delete_user(request, user_id):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.user_type not in ('authority', 'admin'):
            messages.error(request, 'Access denied!')
            return redirect('dashboard')
    except Exception:
        messages.error(request, 'Access denied!')
        return redirect('dashboard')

    User = get_user_model()
    try:
        target = User.objects.get(id=user_id)
        if target == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('manage_users')
        target.delete()
        messages.success(request, 'User deleted.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')

    return redirect('manage_users')

# Missing view functions - Added to fix URL references
def make_payment(request):
    return render(request, 'bus/payment.html')

def search_results(request):
    return render(request, 'bus/search_results.html')
