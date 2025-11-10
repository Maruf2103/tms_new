from django.core.management.base import BaseCommand
from django.utils import timezone
from buses.models import Bus, Route, Schedule
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Creates sample bus schedules for UAP students'

    def handle(self, *args, **options):
        # Create common UAP routes
        routes = [
            {
                'name': 'UAP Campus - Farmgate',
                'start': 'UAP Campus',
                'end': 'Farmgate',
                'stops': 'UAP Campus, Green Road, Panthapath, Farmgate',
                'distance': 5.2,
                'time': 30,
                'fare': 25.00
            },
            {
                'name': 'UAP Campus - Mohakhali',
                'start': 'UAP Campus',
                'end': 'Mohakhali',
                'stops': 'UAP Campus, Green Road, Tejgaon, Mohakhali',
                'distance': 6.5,
                'time': 35,
                'fare': 30.00
            },
            {
                'name': 'UAP Campus - Mirpur',
                'start': 'UAP Campus',
                'end': 'Mirpur-10',
                'stops': 'UAP Campus, Agargaon, IDB, Mirpur-10',
                'distance': 8.0,
                'time': 45,
                'fare': 35.00
            },
            {
                'name': 'UAP Campus - Uttara',
                'start': 'UAP Campus',
                'end': 'Uttara Sector-10',
                'stops': 'UAP Campus, Agargaon, Airport, Uttara',
                'distance': 15.0,
                'time': 60,
                'fare': 45.00
            },
            {
                'name': 'UAP Campus - Motijheel',
                'start': 'UAP Campus',
                'end': 'Motijheel',
                'stops': 'UAP Campus, Shahbag, Paltan, Motijheel',
                'distance': 7.5,
                'time': 40,
                'fare': 30.00
            }
        ]

        # Create buses
        buses = [
            ('UAP-001', 'Campus Express 1', 40),
            ('UAP-002', 'Campus Express 2', 40),
            ('UAP-003', 'Campus Express 3', 40),
            ('UAP-004', 'Campus Express 4', 40),
            ('UAP-005', 'Campus Express 5', 40)
        ]

        # Create buses first
        created_buses = []
        for bus_number, bus_name, capacity in buses:
            bus, created = Bus.objects.get_or_create(
                bus_number=bus_number,
                defaults={
                    'bus_name': bus_name,
                    'capacity': capacity,
                    'driver_name': f'Driver {bus_number}',
                    'is_active': True
                }
            )
            created_buses.append(bus)
            if created:
                self.stdout.write(f'Created bus: {bus_name}')

        # Create routes
        created_routes = []
        for route in routes:
            route_obj, created = Route.objects.get_or_create(
                route_name=route['name'],
                defaults={
                    'start_point': route['start'],
                    'end_point': route['end'],
                    'stops': route['stops'],
                    'distance': route['distance'],
                    'estimated_time': route['time'],
                    'fare': route['fare']
                }
            )
            created_routes.append(route_obj)
            if created:
                self.stdout.write(f'Created route: {route["name"]}')

        # Create schedules for the next 7 days
        # Morning to evening schedule times
        schedule_times = [
            ('07:00', '07:45'),  # Early morning
            ('08:00', '08:45'),  # Morning rush
            ('09:30', '10:15'),  # Late morning
            ('11:00', '11:45'),  # Pre-noon
            ('12:30', '13:15'),  # Lunch time
            ('14:00', '14:45'),  # Early afternoon
            ('15:30', '16:15'),  # Late afternoon
            ('17:00', '17:45'),  # Evening rush
            ('18:00', '18:45'),  # Evening
            ('19:00', '19:45')   # Late evening
        ]

        # Get today's date
        today = timezone.now().date()

        # Create schedules for each day
        for day_offset in range(7):  # Next 7 days
            schedule_date = today + timedelta(days=day_offset)
            
            # For each route
            for route in created_routes:
                # For each time slot
                for departure, arrival in schedule_times:
                    # Rotate through buses
                    bus = created_buses[day_offset % len(created_buses)]
                    
                    # Create schedule
                    schedule, created = Schedule.objects.get_or_create(
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
                    
                    if created:
                        self.stdout.write(
                            f'Created schedule: {schedule_date} {departure} - {route.route_name}'
                        )

        self.stdout.write(self.style.SUCCESS('Successfully created sample schedules'))