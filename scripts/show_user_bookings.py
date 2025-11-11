import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uap_tms.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from buses.models import Booking, MonthlySubscription

User = get_user_model()

username = 'maruf123'
try:
    user = User.objects.get(username=username)
except User.DoesNotExist:
    print(f'User {username} not found')
    sys.exit(1)

print(f'User: {user} (id={user.id})')

print('\nBookings for user:')
qs = Booking.objects.filter(user=user).order_by('-booking_date')
if not qs.exists():
    print('  No bookings')
else:
    for b in qs:
        print(f'  Booking {b.booking_id} | status={b.payment_status} | confirmed={b.is_confirmed} | passengers={b.passengers} | total={b.total_amount} | booked_at={b.booking_date}')
        try:
            print(f'    Schedule: id={b.schedule.id} date={b.schedule.date} dep={b.schedule.departure_time} route={b.schedule.route.route_name}')
        except Exception:
            pass

print('\nMonthly Subscriptions for user:')
ms = MonthlySubscription.objects.filter(user=user).order_by('-created_at')
if not ms.exists():
    print('  No subscriptions')
else:
    for s in ms:
        print(f'  Subscription {s.subscription_id} | status={s.payment_status} | active={s.is_active} | passengers={s.passengers} | amount={s.monthly_amount} | start={s.start_date} end={s.end_date} created={s.created_at}')
        try:
            print(f'    Schedule: id={s.schedule.id} date={s.schedule.date} dep={s.schedule.departure_time} route={s.schedule.route.route_name}')
        except Exception:
            pass

print('\nEnd')
