from django.db import migrations
from django.utils import timezone
from datetime import datetime, timedelta

def create_initial_data(apps, schema_editor):
    Bus = apps.get_model('buses', 'Bus')
    Route = apps.get_model('buses', 'Route')
    Schedule = apps.get_model('buses', 'Schedule')

    # Create buses
    buses_data = [
        {
            'bus_number': 'UAP-001',
            'bus_name': 'Campus Express 1',
            'capacity': 40,
        },
        {
            'bus_number': 'UAP-002',
            'bus_name': 'Campus Express 2',
            'capacity': 40,
        },
        {
            'bus_number': 'UAP-003',
            'bus_name': 'Campus Express 3',
            'capacity': 40,
        },
        {
            'bus_number': 'UAP-004',
            'bus_name': 'Campus Express 4',
            'capacity': 40,
        },
        {
            'bus_number': 'UAP-005',
            'bus_name': 'Campus Express 5',
            'capacity': 40,
        },
    ]

    buses = []
    for bus_data in buses_data:
        bus = Bus.objects.create(**bus_data)
        buses.append(bus)

    # Create routes
    routes_data = [
        {
            'route_name': 'UAP-Farmgate Route',
            'start_point': 'UAP Campus',
            'end_point': 'Farmgate',
            'stops': 'UAP Campus, Green Road, Panthapath, Farmgate',
            'distance': 5.2,
            'estimated_time': 30,
            'fare': 25.00,
        },
        {
            'route_name': 'UAP-Mohakhali Route',
            'start_point': 'UAP Campus',
            'end_point': 'Mohakhali',
            'stops': 'UAP Campus, Green Road, Tejgaon, Mohakhali',
            'distance': 6.5,
            'estimated_time': 35,
            'fare': 30.00,
        },
        {
            'route_name': 'UAP-Mirpur Route',
            'start_point': 'UAP Campus',
            'end_point': 'Mirpur-10',
            'stops': 'UAP Campus, Agargaon, IDB, Mirpur-10',
            'distance': 8.0,
            'estimated_time': 45,
            'fare': 35.00,
        },
        {
            'route_name': 'UAP-Uttara Route',
            'start_point': 'UAP Campus',
            'end_point': 'Uttara Sector-10',
            'stops': 'UAP Campus, Agargaon, Airport, Uttara',
            'distance': 15.0,
            'estimated_time': 60,
            'fare': 45.00,
        },
        {
            'route_name': 'UAP-Motijheel Route',
            'start_point': 'UAP Campus',
            'end_point': 'Motijheel',
            'stops': 'UAP Campus, Shahbag, Paltan, Motijheel',
            'distance': 7.5,
            'estimated_time': 40,
            'fare': 30.00,
        },
    ]

    routes = []
    for route_data in routes_data:
        route = Route.objects.create(**route_data)
        routes.append(route)

    # Create schedules for the next 7 days
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
        ('19:00', '19:45'),
    ]

    today = timezone.now().date()

    for day_offset in range(7):
        schedule_date = today + timedelta(days=day_offset)
        
        for route in routes:
            for i, (departure, arrival) in enumerate(schedule_times):
                bus = buses[i % len(buses)]
                
                Schedule.objects.create(
                    bus=bus,
                    route=route,
                    date=schedule_date,
                    departure_time=departure,
                    arrival_time=arrival,
                    available_seats=bus.capacity,
                    is_active=True
                )

def remove_initial_data(apps, schema_editor):
    Bus = apps.get_model('buses', 'Bus')
    Route = apps.get_model('buses', 'Route')
    Schedule = apps.get_model('buses', 'Schedule')

    Schedule.objects.all().delete()
    Route.objects.all().delete()
    Bus.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('buses', '0001_initial'),  # Update this to your last migration
    ]

    operations = [
        migrations.RunPython(create_initial_data, remove_initial_data),
    ]