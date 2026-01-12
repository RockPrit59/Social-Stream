import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 1. Get the User who is connecting (Me)
        self.me = self.scope['user']
        
        # 2. Get the User I want to talk to (from URL)
        # Note: In routing.py we called this 'room_name'
        self.other_user = self.scope['url_route']['kwargs']['room_name']

        # 3. CRITICAL FIX: Sort the names!
        # This ensures "Prit talking to Pritam" and "Pritam talking to Prit"
        # both end up in the EXACT SAME room: "chat_Prit_Pritam"
        if self.me.username < self.other_user:
            self.room_group_name = f"chat_{self.me.username}_{self.other_user}"
        else:
            self.room_group_name = f"chat_{self.other_user}_{self.me.username}"

        # 4. Join the Room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the Room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (Browser)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json.get('username', self.me.username)

        # Send message to the Room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from Room
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket (Browser)
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))