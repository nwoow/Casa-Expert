import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['user'])
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            self.user = self.scope['user']
            self.group_name = f'user_{self.user}'
            print(self.group_name)
            # Join user-specific group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Send message to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'task_message',
                'message': message
            }
        )

    async def disconnect(self, close_code):
        #Leave user-specific group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        

    async def task_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))