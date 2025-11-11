import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uap_tms.settings')
import django
django.setup()

from buses.models import Booking
from django.contrib.auth import get_user_model
User = get_user_model()

# Print bookings grouped by user and status
from collections import defaultdict
by_user = defaultdict(lambda: defaultdict(int))
for b in Booking.objects.all():
    by_user[str(b.user)][b.payment_status] += 1

for user, statuses in by_user.items():
    print('User:', user)
    total = sum(statuses.values())
    print('  Total bookings:', total)
    for st, cnt in statuses.items():
        print(f'   {st}: {cnt}')
    print('  Visible (excluding cancelled):', total - statuses.get('cancelled', 0))
    print()
