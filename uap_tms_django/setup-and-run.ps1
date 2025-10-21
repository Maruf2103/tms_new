# setup-and-run.ps1 - Complete Django TMS Setup
Write-Host "?? UAP-TMS Django Setup and Launch" -ForegroundColor Cyan

# Step 1: Run migrations
Write-Host "`n?? Setting up database..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

# Step 2: Create superuser (if not exists)
Write-Host "`n?? Creating admin user..." -ForegroundColor Yellow
$adminCheck = python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@uap.edu.bd', 'admin123')
    print('Admin user created: admin / admin123')
else:
    print('Admin user already exists')
"

Write-Host $adminCheck -ForegroundColor Green

# Step 3: Create demo data
Write-Host "`n?? Creating demo data..." -ForegroundColor Yellow
python manage.py shell -c "
from transportation.models import *
from django.contrib.auth.models import User
import datetime

# Create demo users if not exists
if not User.objects.filter(username='student1').exists():
    user1 = User.objects.create_user('student1', 'student1@uap.edu.bd', 'password123')
    user1.first_name = 'Samia Zaman'
    user1.save()
    UserProfile.objects.create(user=user1, user_type='student', phone='01700123456', department='CSE', student_id='23101174')

if not User.objects.filter(username='faculty1').exists():
    user2 = User.objects.create_user('faculty1', 'faculty1@uap.edu.bd', 'password123')
    user2.first_name = 'Dr. Atia Rahman'
    user2.save()
    UserProfile.objects.create(user=user2, user_type='faculty', phone='01800123456', department='CSE')

# Create demo buses if not exists
if not Bus.objects.exists():
    buses_data = [
        {'bus_number': 'UAP-BUS-01', 'route': 'Mirpur to UAP Campus', 'departure_time': '08:00:00', 'capacity': 40, 'available_seats': 25, 'driver_name': 'Abdul Karim', 'driver_phone': '01700123459'},
        {'bus_number': 'UAP-BUS-02', 'route': 'Dhanmondi to UAP Campus', 'departure_time': '08:30:00', 'capacity': 40, 'available_seats': 18, 'driver_name': 'Mohammad Ali', 'driver_phone': '01700123460'},
        {'bus_number': 'UAP-BUS-03', 'route': 'Gulshan to UAP Campus', 'departure_time': '09:00:00', 'capacity': 40, 'available_seats': 40, 'driver_name': 'Rahim Khan', 'driver_phone': '01700123461'},
    ]
    
    for bus_data in buses_data:
        Bus.objects.create(**bus_data)

print('Demo data created successfully!')
"

Write-Host "? Demo data created" -ForegroundColor Green

# Step 4: Run the server
Write-Host "`n?? Starting UAP-TMS Django Server..." -ForegroundColor Cyan
Write-Host "?? User Application: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "?? Admin Panel (via views): http://127.0.0.1:8000/admin-panel/" -ForegroundColor Yellow
Write-Host "??  Django Admin: http://127.0.0.1:8000/admin" -ForegroundColor Blue
Write-Host "`n?? Demo Accounts:" -ForegroundColor White
Write-Host "   Admin: admin / admin123" -ForegroundColor Cyan
Write-Host "   Student: student1 / password123" -ForegroundColor Cyan
Write-Host "   Faculty: faculty1 / password123" -ForegroundColor Cyan

python manage.py runserver
