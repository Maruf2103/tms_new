import random
import time
from django.core.management.base import BaseCommand
from django.test import Client

class Command(BaseCommand):
    help = 'Simulates live GPS updates for Bus and Minibus vehicles'

    def handle(self, *args, **options):
        client = Client()
        # Use vehicle_id values that EXIST in your Vehicle model
        vehicles = ['BUS-01', 'MINIBUS-01']  # ← Must match your DB entries
        lat, lng = 23.7104, 90.4074  # Default: Dhaka (update to your university location)

        self.stdout.write(
            self.style.SUCCESS('Starting GPS simulation... Press Ctrl+C to stop.')
        )

        try:
            while True:
                for vid in vehicles:
                    # Simulate small movement (about 100–200 meters)
                    lat += random.uniform(-0.0005, 0.0005)
                    lng += random.uniform(-0.0005, 0.0005)

                    response = client.post('/tracking/update-location/', {
                        'vehicle_id': vid,
                        'latitude': f"{lat:.6f}",
                        'longitude': f"{lng:.6f}",
                    })

                    '''if response.status_code == 200:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✅ Updated {vid} → ({lat:.6f}, {lng:.6f})"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f"❌ Failed to update {vid}: {response.content}"
                            )
                        )'''

                time.sleep(3)  # Update every 3 seconds

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nSimulation stopped.'))