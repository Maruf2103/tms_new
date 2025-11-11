import os,sys
BASE_DIR = r'E:/3rdyear/2nd_sem/TSM/TMS'
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uap_tms.settings')

import django
django.setup()

from django.utils import timezone
from django.db.models import Q
from buses.models import Schedule

now = timezone.localtime()
today = now.date()
current_time = now.time()

qs = Schedule.objects.filter(is_active=True).filter(
    Q(date__gt=today) | (Q(date=today) & Q(departure_time__gte=current_time))
)

print('now:', now)
print('count upcoming schedules (filtered):', qs.count())
print('sample:')
for s in qs.select_related('route','bus')[:5]:
    print({'id': s.id, 'date': str(s.date), 'departure_time': str(s.departure_time), 'route': getattr(s.route, 'name', None), 'bus': getattr(s.bus, 'registration_number', None), 'available_seats': s.available_seats})
