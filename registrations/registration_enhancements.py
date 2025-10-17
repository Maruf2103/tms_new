# Extends existing registration without modifying it
from datetime import datetime


class RegistrationEnhancer:
    def __init__(self):
        self.route_preferences = {}

    def suggest_routes(self, user_department, preferred_time):
        """Suggest optimal routes based on department and time"""
        suggestions = {
            'morning': ['Route A - 8:00 AM', 'Route B - 8:30 AM'],
            'afternoon': ['Route C - 2:00 PM', 'Route D - 3:00 PM'],
            'evening': ['Route E - 5:00 PM', 'Route F - 6:00 PM']
        }
        return suggestions.get(preferred_time, [])

    def check_seat_availability(self, bus_id, date):
        """Check available seats for a bus on specific date"""
        # Simulate seat availability
        return {
            'bus_id': bus_id,
            'date': date,
            'available_seats': 25,
            'total_seats': 40,
            'waitlist': 0
        }


registration_enhancer = RegistrationEnhancer()