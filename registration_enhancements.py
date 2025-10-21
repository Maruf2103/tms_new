# registration_enhancements.py - Enhanced registration features
from datetime import datetime, timedelta
import random

class RegistrationEnhancer:
    def __init__(self):
        self.route_preferences = {}
        self.peak_hours = {
            'morning': ['07:00-09:00'],
            'afternoon': ['14:00-15:00'],
            'evening': ['17:00-19:00']
        }
    
    def suggest_routes(self, user_department, preferred_time):
        """Suggest optimal routes based on department and time"""
        department_routes = {
            'CSE': ['Route A - CSE Building', 'Route B - Main Gate'],
            'EEE': ['Route C - EEE Building', 'Route D - South Gate'],
            'BBA': ['Route E - BBA Building', 'Route F - North Gate'],
            'default': ['Route G - Central', 'Route H - Campus Ring']
        }
        
        time_suggestions = {
            'morning': ['Early Bird Special', 'Peak Hour Express'],
            'afternoon': ['Afternoon Regular', 'Class Break Special'],
            'evening': ['Evening Service', 'Late Study Route']
        }
        
        routes = department_routes.get(user_department, department_routes['default'])
        times = time_suggestions.get(preferred_time, ['Standard Route'])
        
        return {
            'department_routes': routes,
            'time_based_suggestions': times,
            'recommended': f"{routes[0]} - {times[0]}"
        }
    
    def check_seat_availability(self, bus_id, date):
        """Check available seats for a bus on specific date"""
        # Simulate seat availability with some randomness
        base_seats = 40
        available = random.randint(15, 35)
        waitlist = max(0, base_seats - available - random.randint(0, 10))
        
        return {
            'bus_id': bus_id,
            'date': date,
            'available_seats': available,
            'total_seats': base_seats,
            'waitlist': waitlist,
            'occupancy_rate': f"{((base_seats - available) / base_seats) * 100:.1f}%"
        }
    
    def get_peak_hour_suggestions(self):
        """Get suggestions for avoiding peak hours"""
        return {
            'avoid_times': self.peak_hours,
            'suggestions': [
                'Try traveling 30 minutes before or after peak hours',
                'Consider alternative routes during busy times',
                'Book in advance for guaranteed seats'
            ]
        }
    
    def calculate_estimated_arrival(self, route, start_time):
        """Calculate estimated arrival time"""
        # Simple estimation logic
        route_durations = {
            'Route A': 45,
            'Route B': 35,
            'Route C': 50,
            'Route D': 40
        }
        
        duration = route_durations.get(route, 30)
        arrival_time = datetime.strptime(start_time, '%H:%M') + timedelta(minutes=duration)
        
        return {
            'route': route,
            'departure': start_time,
            'estimated_arrival': arrival_time.strftime('%H:%M'),
            'duration_minutes': duration
        }

registration_enhancer = RegistrationEnhancer()
print("? Registration Enhancements Module Loaded")
