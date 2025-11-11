import os
import sys
import django
from collections import Counter

# Ensure project root is on sys.path so 'uap_tms' settings module can be imported
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uap_tms.settings')
django.setup()

from django.utils import timezone
from buses.models import Schedule

local = timezone.localdate()
utcnow_date = timezone.now().date()

print('timezone.localdate():', local)
print('timezone.now().date():', utcnow_date)

# Count schedules per date
dates = list(Schedule.objects.values_list('date', flat=True))
counts = Counter(dates)

# Print counts for today, yesterday, tomorrow
from datetime import timedelta
print('Count for local today:', counts.get(local, 0))
print('Count for utcnow date:', counts.get(utcnow_date, 0))
print('Distinct dates in DB (sorted):')
for d in sorted(counts.keys()):
    print(d, counts[d])

# Print a small sample of schedules for local today and for utcnow_date
print('\nSample schedules for local today:')
for s in Schedule.objects.filter(date=local)[:10]:
    print(s.id, s.date, s.departure_time, s.route.route_name)

print('\nSample schedules for timezone.now().date():')
for s in Schedule.objects.filter(date=utcnow_date)[:10]:
    print(s.id, s.date, s.departure_time, s.route.route_name)
