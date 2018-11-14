# chat/consumers.py

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
import json
from .models import Chat, Message


class ChatConsumer1(JsonWebsocketConsumer):
    def connect(self):

        if self.scope['user'].is_anonymous:
            self.close()
        else:
            self.accept()
        self.chats = set()

    def receive_json(self, content):

        command = content.get('command', None)
        print(content)
        if command:
            if command == "join":
                self.join_chat(content['chat'])

            elif command == "leave":
                self.leaf_chat(content['chat'])

            elif command == "send":

                self.send_chat(content['chat'], content['message'])

    def disconnect(self, close_code):
        chats = self.chats.copy()
        for slug in chats:
            self.leaf_chat(slug)

    def join_chat(self, slug):
        chat = Chat.objects.get(slug=slug)
        self.chats.add(slug)

        async_to_sync(self.channel_layer.group_send(
            chat.slug,
            {
                "type": "chat.join",
                "room_id": slug,
                "username": self.scope["user"].username,
            })
        )

        async_to_sync(self.channel_layer.group_add)(
            chat.slug,
            self.channel_name
        )

        async_to_sync(
            self.send_json(
                {
                    'join': str(slug),
                    'title': chat.name,
                })
        )

    def leaf_chat(self, slug):
        chat = Chat.objects.get(slug=slug)
        self.chats.discard(slug)
        async_to_sync(self.channel_layer.group_send(
            chat.slug,
            {
                "type": "chat.leaf",
                "room_id": slug,
                "username": self.scope["user"].username,
            })
        )

        async_to_sync(self.channel_layer.group_discard)(
            chat.slug,
            self.channel_name
        )

        async_to_sync(
            self.send_json(
                {
                    'leaf': str(slug),
                })
        )

    def send_chat(self, chat_slug, message):

        if chat_slug in self.chats:
            chat = Chat.objects.get(slug=chat_slug)
            user = self.scope['user']
            new_message = Message(chat=chat, user=user, text=message)
            new_message.save()

            async_to_sync(self.channel_layer.group_send)(
                chat.slug,
                {
                    'type': 'chat.message',
                    'chat': chat_slug,
                    'username': user.username,
                    'message': new_message.text,
                    'date': "{:%m - %d - %Y}".format(new_message.date),
                }
            )

    def chat_join(self, event):
        async_to_sync(self.send_json(
            {
                "msg_type": 1,
                "chat": event["room_id"],
                "username": event["username"],
            },
        ))

    def chat_leaf(self, event):
        async_to_sync(self.send_json(
            {
                "msg_type": 2,
                "chat": event["room_id"],
                "username": event["username"],
            },
        ))

    def chat_message(self, event):
        print(event)
        async_to_sync(self.send_json(
            {
                "msg_type": 0,
                "chat": event["chat"],
                "username": event["username"],
                "message": event["message"],
            },
        ))


'''
class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
'''
