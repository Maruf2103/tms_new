import sys, os
BASE_DIR = r'E:/3rdyear/2nd_sem/TSM/TMS'
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uap_tms.settings')

import django
django.setup()
from django.contrib.auth import get_user_model
from buses.models import UserProfile

if len(sys.argv) < 2:
    print('Usage: python set_user_authority.py <username>')
    sys.exit(1)

username = sys.argv[1]
User = get_user_model()
try:
    u = User.objects.get(username=username)
except User.DoesNotExist:
    print('User not found:', username)
    sys.exit(2)

u.is_staff = True
u.is_active = True
u.save()

profile, created = UserProfile.objects.get_or_create(user=u)
profile.user_type = 'authority'
profile.save()

print('Updated user:', u.username, 'is_staff=', u.is_staff, 'profile_user_type=', profile.user_type, 'profile_created=', created)
