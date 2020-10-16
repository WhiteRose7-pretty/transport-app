from django.shortcuts import render, redirect
from dashboard.models import NewOrder
from django.contrib.auth.decorators import login_required
from chat.models import get_chatList, Contact


def products(request):
    nav_activate = 2
    user_products = NewOrder.objects.all().order_by('-updated_at')

    context ={'nav_activate': nav_activate,
              'user_products': user_products}
    return render(request, 'company/products.html', context)


@login_required(login_url='/uwierzytelnienie/')
def chat(request):
    chat_list = get_chatList(request.user)
    if chat_list.first():
        first_room = str(chat_list.first().pk)
    else:
        first_room = '0'

    if request.user.company:
        return redirect('/profil-firmowy/chat/' + first_room)
    else:
        return redirect('/')


@login_required(login_url='/uwierzytelnienie/')
def chat0(request, room_name):
    nav_activate = 1
    global friend
    friends = []
    chat_list = get_chatList(request.user)
    contact = Contact.objects.get(user=request.user)
    for chat in chat_list:
        for partner in chat.participants.all():
            if partner.user.username != request.user.username:
                chat.other = partner.user
                print(chat.other.online)
                friends.append(chat.other)

        if str(chat.pk) == room_name:
            friend = chat.other
        messages = chat.messages.all()
        chat.other_status = messages.last()
        # chat.unreads = chat.messages.exclude(contact=user_contact).filter(read=0).count()
    context = {
        'nav_activate': nav_activate,
        'username': request.user.username,
        'contact_name': contact.pk,
        'contact': chat_list,
        'room_name': room_name,
        'friend': friend,
    }
    if request.user.company:
        return render(request, 'company/chat.html', context)
    else:
        return redirect('/')