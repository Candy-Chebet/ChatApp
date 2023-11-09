import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from . import AES_encryption

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        username = data.get('username')
        room = data.get('room')

        if message and username and room:
            # Encrypt the message before saving it
            encrypted_message = AES_encryption.encrypt_message_with_password(
                user_password="YourPassword",  # Replace with your encryption password
                plaintext=message,
                salt="YourSalt"  # Replace with your salt value
            )

            await self.save_message(username, room, encrypted_message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': encrypted_message,
                    'username': username
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Decrypt the received message before sending it to the client
        decrypted_message = AES_encryption.decrypt_message_with_password(
            user_password="YourPassword",  # Replace with your encryption password
            ciphertext=message,
            salt="YourSalt"  # Replace with your salt value
        )

        await self.send(text_data=json.dumps({
            'message': decrypted_message,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)
