# create-all-files.ps1 - Create all missing modules for UAP-TMS
Write-Host "?? Creating all required modules for UAP-TMS..." -ForegroundColor Cyan

# 1. Create realtime_tracking.py
@"
# realtime_tracking.py - Real-time bus location tracking
import json
from datetime import datetime
import random

class LiveLocationTracker:
    def __init__(self):
        self.vehicle_locations = {}
    
    def update_bus_location(self, bus_id, lat, lng):
        """Update bus location - can be simulated for demo"""
        self.vehicle_locations[bus_id] = {
            'latitude': lat,
            'longitude': lng, 
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'speed': f'{random.randint(20, 40)} km/h',
            'status': 'moving',
            'route': f'Route {bus_id} - UAP Campus'
        }
        return True
    
    def get_bus_location(self, bus_id):
        """Get current bus location"""
        return self.vehicle_locations.get(bus_id, {})
    
    def get_all_locations(self):
        """Get all bus locations for dashboard"""
        return self.vehicle_locations

    def simulate_bus_movement(self, bus_id, base_lat, base_lng):
        """Simulate bus movement for demo purposes"""
        new_lat = base_lat + random.uniform(-0.001, 0.001)
        new_lng = base_lng + random.uniform(-0.001, 0.001)
        self.update_bus_location(bus_id, new_lat, new_lng)
        return new_lat, new_lng

# Singleton instance
tracker = LiveLocationTracker()

# Demo data initialization
def initialize_demo_data():
    """Initialize with demo bus locations"""
    demo_buses = {
        1: {'lat': 23.7806, 'lng': 90.4193, 'route': 'Mirpur to UAP'},
        2: {'lat': 23.7506, 'lng': 90.3893, 'route': 'Dhanmondi to UAP'},
        3: {'lat': 23.7706, 'lng': 90.4293, 'route': 'Gulshan to UAP'}
    }
    
    for bus_id, data in demo_buses.items():
        tracker.update_bus_location(bus_id, data['lat'], data['lng'])
    
    print(f"? Demo data initialized with {len(demo_buses)} buses")
    return len(demo_buses)

# Initialize demo data when module loads
initialize_demo_data()
print("? Real-time Tracking Module Loaded")
"@ | Set-Content -Path "realtime_tracking.py"
Write-Host "? Created: realtime_tracking.py" -ForegroundColor Green

# 2. Create payment_system.py
@"
# payment_system.py - Online payment processing system
from datetime import datetime
import random

class PaymentProcessor:
    def __init__(self):
        self.transactions = {}
        self.payment_methods = ['bkash', 'nagad', 'rocket', 'card']
    
    def process_payment(self, user_id, amount, payment_method="bkash", bus_id=None):
        """Process payment - simulate for demo"""
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}"
        
        # Simulate payment processing
        transaction_data = {
            'transaction_id': transaction_id,
            'user_id': user_id,
            'bus_id': bus_id,
            'amount': amount,
            'payment_method': payment_method,
            'status': 'completed',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'reference': f"REF{random.randint(10000,99999)}"
        }
        
        self.transactions[transaction_id] = transaction_data
        return transaction_data
    
    def verify_payment(self, transaction_id):
        """Verify payment status"""
        return self.transactions.get(transaction_id, {})
    
    def get_user_payments(self, user_id):
        """Get all payments for a user"""
        user_payments = []
        for transaction in self.transactions.values():
            if transaction['user_id'] == user_id:
                user_payments.append(transaction)
        return user_payments
    
    def get_payment_methods(self):
        """Get available payment methods"""
        return self.payment_methods

payment_processor = PaymentProcessor()
print("? Payment System Module Loaded")
"@ | Set-Content -Path "payment_system.py"
Write-Host "? Created: payment_system.py" -ForegroundColor Green

# 3. Create registration_enhancements.py
@"
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
"@ | Set-Content -Path "registration_enhancements.py"
Write-Host "? Created: registration_enhancements.py" -ForegroundColor Green

# 4. Create api_extensions.py
@"
# api_extensions.py - New API endpoints for enhancements
from flask import Blueprint, jsonify, request
from datetime import datetime
from realtime_tracking import tracker
from payment_system import payment_processor
from registration_enhancements import registration_enhancer

api_ext = Blueprint('api_extensions', __name__)

# Real-time Tracking APIs
@api_ext.route('/api/bus/locations', methods=['GET'])
def get_bus_locations():
    """API to get all bus locations"""
    locations = tracker.get_all_locations()
    return jsonify({
        'status': 'success',
        'count': len(locations),
        'locations': locations,
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@api_ext.route('/api/bus/<int:bus_id>/location', methods=['GET'])
def get_bus_location(bus_id):
    """API to get specific bus location"""
    location = tracker.get_bus_location(bus_id)
    if location:
        return jsonify({'status': 'success', 'bus_id': bus_id, 'location': location})
    else:
        return jsonify({'status': 'error', 'message': 'Bus not found'}), 404

@api_ext.route('/api/bus/<int:bus_id>/location', methods=['POST'])
def update_bus_location(bus_id):
    """API to update bus location (for demo)"""
    data = request.json
    if not data or 'lat' not in data or 'lng' not in data:
        return jsonify({'status': 'error', 'message': 'Missing lat/lng data'}), 400
    
    tracker.update_bus_location(bus_id, data.get('lat'), data.get('lng'))
    return jsonify({'status': 'success', 'bus_id': bus_id, 'message': 'Location updated'})

@api_ext.route('/api/bus/<int:bus_id>/simulate-move', methods=['POST'])
def simulate_bus_movement(bus_id):
    """API to simulate bus movement for demo"""
    current_location = tracker.get_bus_location(bus_id)
    if not current_location:
        # Initialize with UAP coordinates if bus doesn't exist
        base_lat, base_lng = 23.7806, 90.4193
    else:
        base_lat, base_lng = current_location['latitude'], current_location['longitude']
    
    new_lat, new_lng = tracker.simulate_bus_movement(bus_id, base_lat, base_lng)
    return jsonify({
        'status': 'success',
        'bus_id': bus_id,
        'new_location': {'lat': new_lat, 'lng': new_lng},
        'message': 'Bus movement simulated'
    })

# Payment System APIs
@api_ext.route('/api/payment/process', methods=['POST'])
def process_payment():
    """API to process payment"""
    data = request.json
    if not data or 'user_id' not in data or 'amount' not in data:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    result = payment_processor.process_payment(
        data.get('user_id'),
        data.get('amount'),
        data.get('payment_method', 'bkash'),
        data.get('bus_id')
    )
    return jsonify({'status': 'success', 'payment': result})

@api_ext.route('/api/payment/verify/<transaction_id>', methods=['GET'])
def verify_payment(transaction_id):
    """API to verify payment"""
    result = payment_processor.verify_payment(transaction_id)
    if result:
        return jsonify({'status': 'success', 'payment': result})
    else:
        return jsonify({'status': 'error', 'message': 'Transaction not found'}), 404

@api_ext.route('/api/payment/methods', methods=['GET'])
def get_payment_methods():
    """API to get available payment methods"""
    methods = payment_processor.get_payment_methods()
    return jsonify({'status': 'success', 'payment_methods': methods})

@api_ext.route('/api/payment/user/<user_id>', methods=['GET'])
def get_user_payments(user_id):
    """API to get user payment history"""
    payments = payment_processor.get_user_payments(user_id)
    return jsonify({'status': 'success', 'user_id': user_id, 'payments': payments})

# Route & Registration APIs
@api_ext.route('/api/routes/suggest', methods=['GET'])
def suggest_routes():
    """API to suggest routes based on time and department"""
    department = request.args.get('department', 'CSE')
    preferred_time = request.args.get('time', 'morning')
    
    suggestions = registration_enhancer.suggest_routes(department, preferred_time)
    return jsonify({'status': 'success', 'suggestions': suggestions})

@api_ext.route('/api/bus/<int:bus_id>/availability', methods=['GET'])
def check_seat_availability(bus_id):
    """API to check seat availability"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    availability = registration_enhancer.check_seat_availability(bus_id, date)
    return jsonify({'status': 'success', 'availability': availability})

@api_ext.route('/api/routes/peak-hours', methods=['GET'])
def get_peak_hours():
    """API to get peak hour information"""
    suggestions = registration_enhancer.get_peak_hour_suggestions()
    return jsonify({'status': 'success', 'peak_hours': suggestions})

@api_ext.route('/api/routes/estimate-arrival', methods=['GET'])
def estimate_arrival():
    """API to estimate arrival time"""
    route = request.args.get('route', 'Route A')
    start_time = request.args.get('start_time', '08:00')
    
    estimation = registration_enhancer.calculate_estimated_arrival(route, start_time)
    return jsonify({'status': 'success', 'estimation': estimation})

# System Status API
@api_ext.route('/api/system/status', methods=['GET'])
def system_status():
    """API to check system status"""
    return jsonify({
        'status': 'operational',
        'service': 'UAP-TMS Enhanced',
        'version': '2.0',
        'features': {
            'real_time_tracking': True,
            'online_payments': True,
            'smart_routing': True,
            'seat_availability': True
        },
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

print("? API Extensions Module Loaded")
"@ | Set-Content -Path "api_extensions.py"
Write-Host "? Created: api_extensions.py" -ForegroundColor Green

Write-Host "`n?? All Python modules created successfully!" -ForegroundColor Green
Write-Host "`n?? Now you can run: python app_enhanced.py" -ForegroundColor Cyan
