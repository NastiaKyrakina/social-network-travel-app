# chat/consumers.py
from django.template.loader import render_to_string
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
                print('5')
                if 'message_id' in content:
                    print('6')
                    self.send_chat(content['chat'], content['message'], content['message_id'])
                else:
                    print('8')
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

    def send_chat(self, chat_slug, message, message_id=-1):
        print(self.chats)
        if chat_slug in self.chats:
            print('111')
            chat = Chat.objects.get(slug=chat_slug)
            user = self.scope['user']
            if message_id != -1:
                print('to')
                new_message = Message.objects.get(id=message_id)
            else:
                new_message = Message(chat=chat, user=user, text=message)
                new_message.save()

            message_block = render_to_string('Chat/message_block.html', {'message': new_message})

            print(message_block)
            content = {
                'type': 'chat.message',
                'chat': chat_slug,
                'message': message_block,
            }

            async_to_sync(self.channel_layer.group_send)(chat.slug, content)

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
