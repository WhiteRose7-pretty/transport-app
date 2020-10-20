from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from authentication.models import UserHelpedElement, CompanyUserData, CustomUser
from chat.models import get_chatList, Contact, Chat
from .forms import EditAccountBasicInformation, EditPasswordForm, EditCompanyDataForm, ContactPhoneForm, \
    EmailContactForm
from .models import NewOrder


def check_contact(user):
    #user is  admin
    admin_user = CustomUser.objects.get(company=True)
    admin_contact = Contact.objects.get(user__pk=admin_user.pk)
    if user.company:
        pass
    else:
        #check if user have contact, then pass or create
        contacts = Contact.objects.filter(user=user)
        if len(contacts) < 1:
            contact = Contact()
            contact.user = user
            contact.save()
        else:
            contact = Contact.objects.get(user__pk=user.pk)
        #if chat is created then pass or create
        if not Chat.objects.filter(participants=contact):
            chat = Chat()
            chat.save()
            chat.participants.add(contact)
            chat.participants.add(admin_contact)
            chat.save()
        else:
            chat = Chat.objects.filter(participants=contact).first()


@login_required(login_url='/uwierzytelnienie/')
def chat(request):
    check_contact(request.user)
    chat_list = get_chatList(request.user)
    if chat_list.first():
        first_room = str(chat_list.first().pk)
    else:
        first_room = '0'
    if not request.user.company:
        return redirect('/profil/chat/' + first_room + '/')
    else:
        return redirect('/profil-firmowy/chat/' + first_room + '/')



@login_required(login_url='/uwierzytelnienie/')
def chat0(request, room_name):
    check_contact(request.user)
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
    if not request.user.company:
        return render(request, 'dashboard/chat.html', context)
    else:
        return redirect('/profil-firmowy/czat/')



@login_required(login_url='/uwierzytelnienie/')
def products(request):
    nav_activate = 2
    user_products = NewOrder.objects.filter(owner=request.user).order_by('-updated_at')

    context = {'nav_activate': nav_activate,
               'user_products': user_products}
    return render(request, 'dashboard/products.html', context)


@login_required(login_url='/uwierzytelnienie/')
def settings(request):
    # basic information
    nav_activate = 3
    basic_user_data = UserHelpedElement.objects.filter(owner=request.user).last()
    company_data_object = CompanyUserData.objects.filter(owner=request.user).last()
    send = request.session.get('send')
    if send:
        request.session['send'] = None
    send_error = request.session.get('send_error')
    if send_error:
        request.session['send_error'] = None

    # edit user data
    if request.method == 'POST' and 'buttonAccount' in request.POST:
        form_user_data = EditAccountBasicInformation(request.POST, request.FILES)
        if form_user_data.is_valid():
            cd = form_user_data.cleaned_data
            object = UserHelpedElement()
            object.owner = request.user
            object.name = cd['name']

            user_obj = CustomUser.objects.get(pk=request.user.pk)
            user_obj.username = cd['name']
            print(cd['profile_img'])
            user_obj.profile_picture = cd['profile_img']
            user_obj.save()

            object.surname = cd['surname']
            object.save()
            request.session['send'] = 'Twoje informacje o koncie zostały pomyślnie zapisane.'
            return HttpResponseRedirect(reverse('dashboard:settings'))
    else:
        if basic_user_data:
            form_user_data = EditAccountBasicInformation(initial={'name': basic_user_data.name,
                                                                  'surname': basic_user_data.surname})
        else:
            form_user_data = EditAccountBasicInformation()

    # change password
    if request.method == 'POST' and 'buttonPasswordChange' in request.POST:
        security_form = EditPasswordForm(request.POST)
        if security_form.is_valid():
            currentpassword = request.user.password
            currentpasswordentered = security_form.cleaned_data.get('lastpassword')
            password1 = security_form.cleaned_data.get('newpassword1')
            password2 = security_form.cleaned_data.get('newpassword2')
            matchcheck = check_password(currentpasswordentered, currentpassword)
            if matchcheck and password1 == password2:
                user = request.user
                user.set_password(password1)
                user.save()
                request.session['send'] = 'Twoje hasło zostało pomyślnie zmienione.'
                return HttpResponseRedirect(reverse('dashboard:settings'))
            else:
                request.session['send_error'] = 'Wprowadzone przez Ciebie dane nie są poprawne. Spróbój ponownie.'
                return HttpResponseRedirect(reverse('dashboard:settings'))

    else:
        security_form = EditPasswordForm()

    # edit company
    if request.method == 'POST' and 'buttonAdditionalInformation':
        form_company_data = EditCompanyDataForm(request.POST)
        if form_company_data.is_valid():
            cd = form_company_data.cleaned_data
            object = CompanyUserData()
            object.owner = request.user
            object.company_name = cd['company_name']
            object.nip = cd['nip']
            object.province = cd['province']
            object.city = cd['city']
            object.zip_code = cd['zip_code']
            object.street = cd['street']
            object.invoice = cd['invoice']
            object.save()
            request.session['send'] = 'Twoje dane o firmie zostały pomyślnie zapisane.'
            return HttpResponseRedirect(reverse('dashboard:settings'))
    else:
        if company_data_object:
            form_company_data = EditCompanyDataForm(initial={'company_name': company_data_object.company_name,
                                                             'nip': company_data_object.nip,
                                                             'province': company_data_object.province,
                                                             'city': company_data_object.city,
                                                             'zip_code': company_data_object.zip_code,
                                                             'street': company_data_object.street,
                                                             'invoice': company_data_object.invoice})
        else:
            form_company_data = EditCompanyDataForm()

    context = {'form_user_data': form_user_data,
               'form_company_data': form_company_data,
               'security_form': security_form,
               'send_error': send_error,
               'nav_activate': nav_activate,
               'send': send}
    return render(request, 'dashboard/settings.html', context)


@login_required(login_url='/uwierzytelnienie/')
def phone_contact(request):
    nav_activate = 4
    send = request.session.get('send')
    if send:
        request.session['send'] = None

    # phone form
    if request.method == 'POST' and 'buttonSubmitPhoneContact' in request.POST:
        phone_form = ContactPhoneForm(request.POST)
        if phone_form.is_valid():
            cd = phone_form.cleaned_data
            topic = 'Klient prosi o kontakt telefoniczny. | %s | %s | %s |' % (cd['name'], cd['phone'], cd['date'])
            massage = 'Klient prosi o kontakt.'
            to = ['info@transportuj24.pl', ]
            send_mail(topic, massage, 'benjamin.langeriaf7@gmail.com', to)
            request.session['send'] = 'Twoja prośba o kontakt została pomyślnie zapisana.'
            return HttpResponseRedirect(reverse('dashboard:phone_contact'))
    else:
        phone_form = ContactPhoneForm()

    # email phone
    if request.method == 'POST' and 'buttonSubmitEmailContact' in request.POST:
        email_form = EmailContactForm(request.POST)
        if email_form.is_valid():
            cd = email_form.cleaned_data
            topic = 'Klient prosi o odpowiedź | %s |' % (cd['email'])
            massage = cd['description']
            to = ['info@transportuj24.pl', ]
            send_mail(topic, massage, 'benjamin.langeriaf7@gmail.com', to)
            request.session['send'] = 'Twoja wiadomość została wysłana.'
            return HttpResponseRedirect(reverse('dashboard:phone_contact'))
    else:
        email_form = EmailContactForm()

    context = {'nav_activate': nav_activate,
               'phone_form': phone_form,
               'email_form': email_form,
               'send': send, }
    return render(request, 'dashboard/phone_contact.html', context)
