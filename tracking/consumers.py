import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("tracking", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("tracking", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Optional: handle incoming messages (e.g., from driver app)
        pass

    # Custom method to broadcast location
    async def send_location_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))