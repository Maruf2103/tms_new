import os
import django

# Ensure Django settings are loaded so this script can run standalone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from buses.models import Schedule, Booking, UserProfile

User = get_user_model()

u, created = User.objects.get_or_create(username='teststudent', defaults={'email':'test@example.com'})
if created:
    u.set_password('pass123')
    u.save()
    UserProfile.objects.get_or_create(user=u, defaults={'user_type':'student'})
else:
    UserProfile.objects.get_or_create(user=u, defaults={'user_type':'student'})

c = Client()
logged = c.login(username='teststudent', password='pass123')
print('logged in:', logged)

s = Schedule.objects.filter(is_active=True).first()
print('schedule id:', s.id if s else None)

if not s:
    print('No active schedule found; abort')
else:
    resp = c.post(f'/book-bus/{s.id}/', {'passengers':1}, follow=True)
    print('status:', resp.status_code)
    print('redirects:', resp.redirect_chain)
    exists = Booking.objects.filter(user=u).exists()
    print('booking exists:', exists)
    if exists:
        b = Booking.objects.filter(user=u).first()
        print('booking id', b.booking_id, 'passengers', b.passengers, 'total', b.total_amount)
