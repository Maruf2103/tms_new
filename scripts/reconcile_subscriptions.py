import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uap_tms.settings')
import django
django.setup()

from buses.models import MonthlySubscription

fixed = 0
for s in MonthlySubscription.objects.filter(payment_status='completed', seats_reserved=False):
    try:
        sched = s.schedule
        print(f"Reserving {s.passengers} seats on schedule {sched.id} for subscription {s.subscription_id}")
        sched.available_seats = max(0, sched.available_seats - (s.passengers or 0))
        sched.save()
        s.seats_reserved = True
        s.save()
        fixed += 1
    except Exception as e:
        print('Error for', s.subscription_id, e)

print('Done. Fixed:', fixed)
