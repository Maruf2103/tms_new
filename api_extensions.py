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
