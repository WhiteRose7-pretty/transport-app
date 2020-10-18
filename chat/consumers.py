from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.db.models import F

from .models import Message, get_last_10_messages, get_user_contact, get_current_chat, Chat, Contact

User = get_user_model()


def messages_to_json(messages):
    result = []
    for message in messages:
        result.append(message_to_json(message))
    return result


def message_to_json(message):
    contact = message.contact.user
    if contact.profile_picture:
        avatar = contact.profile_picture.url
    else:
        avatar = ''

    if message.file_size != '':
        fileSize = message.file_size
    else:
        fileSize = '0'
    return {
        'id': message.id,
        'contact': contact.username,
        'avatar': avatar,
        'content': message.content,
        'tag': message.tag,
        'file_name': message.file_name,
        'file_url': message.file_url,
        'file_size': sizeof_fmt(int(fileSize)),
        'timestamp': str(message.timestamp)
    }


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def update_user_incr(user):
    currentUser = user
    # currentUser.update(online=F('online') + 1)
    currentUser.online = currentUser.online + 1
    if currentUser.online > 0:
        currentUser.online_s = True
    else:
        currentUser.online_s = False
    currentUser.save()


def update_user_decr(user):
    currentUser = user
    # currentUser.update(online=F('online') - 1)
    currentUser.online = currentUser.online - 1
    if currentUser.online > 0:
        currentUser.online_s = True
    else:
        currentUser.online_s = False
    currentUser.save()


def read_messages(contact, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    chat.messages.exclude(contact=contact).update(read=1)


class ChatConsumer(AsyncWebsocketConsumer):

    async def notification(self, data):
        print('notification')
        user_contact = Contact.objects.get(pk=int(data['contact_name']))
        read_messages(user_contact, data['chatId'])
        await self.send_chat_message(data)

    async def fetch_messages(self, data):  
        messages = get_last_10_messages(data['chatId'])
        content = {
            'command': 'messages',
            'messages': messages_to_json(messages)
        }
        await self.send_message(content)

    async def new_message(self, data):

        user_contact = Contact.objects.get(pk=int(data['contact_name']))
        read_messages(user_contact, data['chatId'])
        message = Message.objects.create(
            contact=user_contact,
            tag=data['tag'],
            file_name=data['message']['file_name'],
            file_url=data['message']['file_url'],
            file_size=data['message']['file_size'],
            content=data['message']['content'],
            read=0)

        current_chat = get_current_chat(data['chatId'])
        current_chat.messages.add(message)
        current_chat.save()

        content = {
            'command': 'new_message',
            'message': message_to_json(message)
        }
        await self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'notification': notification,
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print("connected user:", self.scope['user'])
        update_user_incr(self.scope['user'])
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("disconnected user:", self.scope['user'])
        update_user_decr(self.scope['user'])
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))


