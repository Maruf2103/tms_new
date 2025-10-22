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
