from django import template
import datetime
from authentication.models import CustomUser
from chat.models import Chat

register = template.Library()


@register.simple_tag
def get_new_message(chat, user):
    # check if new messages are in chat for user
    query = chat.messages.filter(read=0).exclude(contact__user=user)
    if len(query):
        return True
    else:
        return False
