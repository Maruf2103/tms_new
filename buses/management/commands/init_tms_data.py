from django.core.management.base import BaseCommand
from django.utils import timezone
from buses.models import Bus, Route, Schedule, UserProfile
from accounts.models import User
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Adds initial data for UAP Transport Management System'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial data for TMS...')

        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@uap.edu',
                password='admin123'
            )
            UserProfile.objects.create(
                user=user,
                user_type='authority',
                phone='01700000000',
                address='UAP Campus'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create buses
        buses_data = [
            ('UAP-001', 'Campus Express 1', 'Mohammad Rahman'),
            ('UAP-002', 'Campus Express 2', 'Abdul Karim'),
            ('UAP-003', 'Campus Express 3', 'Rafiqul Islam'),
            ('UAP-004', 'Campus Express 4', 'Jamal Uddin'),
            ('UAP-005', 'Campus Express 5', 'Kamal Hossain'),
        ]

        for bus_number, bus_name, driver_name in buses_data:
            Bus.objects.get_or_create(
                bus_number=bus_number,
                defaults={
                    'bus_name': bus_name,
                    'driver_name': driver_name,
                    'capacity': 40,
                    'is_active': True
                }
            )

        # Create routes
        routes_data = [
            {
                'name': 'UAP-Farmgate Route',
                'start': 'UAP Campus',
                'end': 'Farmgate',
                'stops': 'UAP Campus, Green Road, Panthapath, Farmgate',
                'distance': 5.2,
                'time': 30,
                'fare': 25.00
            },
            {
                'name': 'UAP-Mohakhali Route',
                'start': 'UAP Campus',
                'end': 'Mohakhali',
                'stops': 'UAP Campus, Green Road, Tejgaon, Mohakhali',
                'distance': 6.5,
                'time': 35,
                'fare': 30.00
            },
            {
                'name': 'UAP-Mirpur Route',
                'start': 'UAP Campus',
                'end': 'Mirpur-10',
                'stops': 'UAP Campus, Agargaon, IDB, Mirpur-10',
                'distance': 8.0,
                'time': 45,
                'fare': 35.00
            },
            {
                'name': 'UAP-Uttara Route',
                'start': 'UAP Campus',
                'end': 'Uttara Sector-10',
                'stops': 'UAP Campus, Agargaon, Airport, Uttara',
                'distance': 15.0,
                'time': 60,
                'fare': 45.00
            },
            {
                'name': 'UAP-Motijheel Route',
                'start': 'UAP Campus',
                'end': 'Motijheel',
                'stops': 'UAP Campus, Shahbag, Paltan, Motijheel',
                'distance': 7.5,
                'time': 40,
                'fare': 30.00
            }
        ]

        for route_data in routes_data:
            Route.objects.get_or_create(
                route_name=route_data['name'],
                defaults={
                    'start_point': route_data['start'],
                    'end_point': route_data['end'],
                    'stops': route_data['stops'],
                    'distance': route_data['distance'],
                    'estimated_time': route_data['time'],
                    'fare': route_data['fare']
                }
            )

        # Create schedules
        schedule_times = [
            ('07:00', '07:45'),
            ('08:00', '08:45'),
            ('09:30', '10:15'),
            ('11:00', '11:45'),
            ('12:30', '13:15'),
            ('14:00', '14:45'),
            ('15:30', '16:15'),
            ('17:00', '17:45'),
            ('18:00', '18:45'),
            ('19:00', '19:45')
        ]

        # Get all buses and routes
        buses = Bus.objects.all()
        routes = Route.objects.all()
        
        # Create schedules for next 7 days
        today = timezone.now().date()
        
        for day_offset in range(7):
            schedule_date = today + timedelta(days=day_offset)
            
            for route in routes:
                for i, (departure, arrival) in enumerate(schedule_times):
                    bus = buses[i % len(buses)]
                    
                    # Create schedule if it doesn't exist
                    Schedule.objects.get_or_create(
                        bus=bus,
                        route=route,
                        date=schedule_date,
                        departure_time=departure,
                        defaults={
                            'arrival_time': arrival,
                            'available_seats': bus.capacity,
                            'is_active': True
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Successfully created initial data'))