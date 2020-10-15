from django.contrib.auth import get_user_model
from django.db import models
from authentication.models import CustomUser
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType


User = get_user_model()


def get_user_contact(user):

    return get_object_or_404(Contact, user=user)


class Contact(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name='friends', on_delete=models.CASCADE)

    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


class Message(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE, default='')
    tag = models.TextField(default='text')
    file_name = models.TextField(default='', blank=True)
    file_url = models.TextField(default='', blank=True)
    file_size = models.TextField(default='', blank=True)
    content = models.TextField(default='', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.DecimalField(max_digits=5, decimal_places=0, default=0)

    def __str__(self):
        return self.contact.user.username


def get_chatList(user):
    queryset = Chat.objects.all()
    if user is not None:
        # contact = get_user_contact(user)
        contact = user.friends.first()
        print(type(contact))
        print(contact)
        queryset = contact.chats.all()
    return queryset


def create_contact(username):
    user = User.objects.filter(username=username)
    Contact.objects.create(
        user=user
    )


def create_chat(username1, username2):
    contact1 = get_user_contact(username1)

    contact2 = get_user_contact(username2)
    chat = Chat()
    chat.save()
    chat.participants.add(contact1, contact2)
    return chat


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)


class Chat(models.Model):
    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, related_name='messages', blank=True)

    def __str__(self):
        return "{}".format(self.pk)