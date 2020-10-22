from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from dashboard.models import NewOrder, CompanyUser
from django.contrib.auth.decorators import login_required
from chat.models import get_chatList, Contact
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import SearchProductForm, PriceProductForm
from chat.models import Chat
from authentication.models import CustomUser




@login_required(login_url='/uwierzytelnienie/')
def products(request):
    nav_activate = 2
    user_products = NewOrder.objects.all().order_by('-updated_at')
    form = SearchProductForm(request.GET)
    date_st_send = request.GET.get('date_st_send')
    date_end_send = request.GET.get('date_end_send')
    category = request.GET.get('category')
    if date_st_send:
        user_products = user_products.filter(date_st_send__gte=date_st_send)
    if date_end_send:
        user_products = user_products.filter(date_end_send__gte=date_end_send)
    if category:
        user_products = user_products.filter(type_product__icontains=category)

    context ={'nav_activate': nav_activate,
              'form': form,
              'user_products': user_products}
    return render(request, 'company/products.html', context)


def check_contact():
    # user is  admin
    admin_user_query = CustomUser.objects.filter(company=True)
    if len(admin_user_query) < 1:
        return False
    admin_user = CustomUser.objects.get(company=True)
    users = CustomUser.objects.filter(company=False)
    admin_contacts = Contact.objects.filter(user__pk=admin_user.pk)
    if len(admin_contacts) < 1:
        admin_contact = Contact()
        admin_contact.user = admin_user
        admin_contact.save()
    else:
        admin_contact = Contact.objects.get(user__pk=admin_user.pk)

    for user in users:
        # check if user have contact, then pass or create
        contacts = Contact.objects.filter(user=user)
        if len(contacts) < 1:
            contact = Contact()
            contact.user = user
            contact.save()
        else:
            contact = Contact.objects.get(user__pk=user.pk)
        # if chat is created then pass or create
        if not Chat.objects.filter(participants=contact):
            chat = Chat()
            chat.save()
            chat.participants.add(contact)
            chat.participants.add(admin_contact)
            chat.save()
        else:
            chat = Chat.objects.filter(participants=contact).first()


@login_required(login_url='/uwierzytelnienie/')
def product_detail(request, id):
    object = get_object_or_404(NewOrder, pk=id)
    nav_activate = 2
    send = request.session.get('send')
    if send:
        request.session['send'] = None

    #forms
    if request.method == 'POST' and 'priceButton' in request.POST:
        form = PriceProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            object.price = cd['price']
            object.save()
            request.session['send'] = 'Cena została pomyślnie zapisana.'
            return HttpResponseRedirect(reverse('company:product_detail', args=[object.id]))
    else:
        form = PriceProductForm()

    context = {'object': object,
               'send': send,
               'form': form,
               'nav_activate': nav_activate}
    return render(request, 'company/product_detail.html', context)



@login_required(login_url='/uwierzytelnienie/')
def mass_message(request):
    nav_activate = 3
    company_query = CompanyUser.objects.all()
    send = request.session.get('send')
    if send:
        request.session['send'] = None

    if request.method == 'POST':
        object_id = request.POST.get('object_id')
        object = get_object_or_404(CompanyUser, pk=int(object_id))
        if object.blocked == True:
            object.blocked = False
        else:
            object.blocked = True
        object.save()
        request.session['send'] = 'Zmiany zostały pomyślnie zapisane.'
        return HttpResponseRedirect(reverse('company:mass_message'))

    context = {'nav_activate': nav_activate,
               'send': send,
               'company_query': company_query}
    return render(request, 'company/mass_message.html', context)



@login_required(login_url='/uwierzytelnienie/')
def chat(request):
    check_contact()
    chat_list = get_chatList(request.user)
    if chat_list.first():
        first_room = str(chat_list.first().pk)
    else:
        return redirect('/')

    if request.user.company:
        return redirect('/profil-firmowy/chat/' + first_room)
    else:
        return redirect('/profil/')



@login_required(login_url='/uwierzytelnienie/')
def chat0(request, room_name):
    check_contact()
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
