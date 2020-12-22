import random
from math import radians, cos, sin, asin, sqrt

import requests
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from dashboard.forms import ContactPhoneForm, EmailContactForm
from dashboard.models import Category, Newsletter, TypeProduct, NewOrder, Przelewy24Transaction
from .additional_functions import code_function, decode_function
from .forms import BasicTypeProductForm, FirstStepForm, Przelewy24PrepareForm
from .models import PrivacyPolicy
from app_rama import settings
import hashlib
from dashboard import choices


def home(request):
    # query
    post_list = Newsletter.objects.all()[:9]
    type_products = TypeProduct.objects.all()
    send = request.session.get('send')
    if send:
        request.session['send'] = None

    # form
    if request.method == 'POST' and 'valuationButtonSubmit' in request.POST:
        form = BasicTypeProductForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            distance = calc_distance(form_data['lat_from'], form_data['lng_from'], form_data['lat_to'],
                                     form_data['lng_to'])
            request.session['lat_from'] = form_data['lat_from']
            request.session['lng_from'] = form_data['lng_from']
            request.session['lat_to'] = form_data['lat_to']
            request.session['lng_to'] = form_data['lng_to']
            request.session['location_from'] = form_data['location_from']
            request.session['location_to'] = form_data['location_to']
            request.session['distance'] = distance
            request.session['type_product'] = form_data['type_product']
            output = {
                'success': True,
            }
        else:
            output = {
                'success': False,
            }
        return JsonResponse(output)

    else:
        form = BasicTypeProductForm()

    if request.method == 'POST' and 'submitContactPhone' in request.POST:
        contact_phone_form = ContactPhoneForm(request.POST)
        if contact_phone_form.is_valid():
            cd = contact_phone_form.cleaned_data
            topic = 'Klient prosi o kontakt telefoniczny. | %s | %s | %s |' % (cd['name'], cd['phone'], cd['date'])
            massage = 'Klient prosi o kontakt.'
            to = ['info@transportuj24.pl', ]
            send_mail(topic, massage, 'info@transportuj24.pl', to)
            request.session['send'] = 'Twoja prośba o kontakt została pomyślnie zapisana.'
            return HttpResponseRedirect(reverse('app:home'))
    else:
        contact_phone_form = ContactPhoneForm()

    if request.method == 'POST' and 'buttonSubmitEmailContact' in request.POST:
        email_form = EmailContactForm(request.POST)
        if email_form.is_valid():
            cd = email_form.cleaned_data
            topic = 'Klient prosi o odpowiedź | %s |' % (cd['email'])
            massage = cd['description']
            to = ['info@transportuj24.pl', ]
            send_mail(topic, massage, 'info@transportuj24.pl', to)
            request.session['send'] = 'Twoja wiadomość została wysłana.'
            return HttpResponseRedirect(reverse('app:home'))
    else:
        email_form = EmailContactForm()

    context = {'post_list': post_list,
               'contact_phone_form': contact_phone_form,
               'email_contact_form': email_form,
               'type_products': type_products,
               'form': form,
               'send': send}
    return render(request, 'app/home.html', context)


def privacy_policy(request):
    special_navbar = True
    document = PrivacyPolicy.objects.last()

    context = {'special_navbar': special_navbar,
               'document': document}
    return render(request, 'app/privacy_policy.html', context)


def terms(request):
    special_navbar = True
    document = PrivacyPolicy.objects.last()

    context = {'special_navbar': special_navbar,
               'document': document}
    return render(request, 'app/terms.html', context)


def blog(request):
    post_list = Newsletter.objects.all()
    category = Category.objects.all()
    logo_white = True
    special_navbar = True

    context = {'post_list': post_list,
               'logo_white': logo_white,
               'special_navbar': special_navbar,
               'category': category}
    return render(request, 'app/blog.html', context)


def article(request, id):
    special_navbar = True
    object = get_object_or_404(Newsletter, pk=id)
    try:
        random_article = random.sample(list(Newsletter.objects.exclude(id=object.id)), 3)
    except:
        random_article = None

    context = {'object': object,
               'special_navbar': special_navbar,
               'random_article': random_article}
    return render(request, 'app/article.html', context)


def valuation(request):
    user = request.user
    if request.method == 'POST':
        form = FirstStepForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            valuation_object = NewOrder()
            valuation_object.type_product = request.session.get('type_product')
            valuation_object.location_name_from = request.session.get('location_from')
            valuation_object.distance = request.session.get('distance')
            valuation_object.org_latitude_form = request.session.get('lat_from')
            valuation_object.org_longitude_from = request.session.get('lng_from')
            valuation_object.location_name_to = request.session.get('location_to')
            valuation_object.org_latitude_to = request.session.get('lat_to')
            valuation_object.org_longitude_to = request.session.get('lng_to')
            valuation_object.depth = cd['length']
            valuation_object.width = cd['width']
            valuation_object.height = cd['height']
            valuation_object.weight = cd['weight']
            valuation_object.quantity = cd['quantity']
            valuation_object.items_descriptions = cd['comments']
            valuation_object.date_st_send = cd['date_st_send']
            valuation_object.date_end_send = cd['date_end_send']
            valuation_object.date_st_received = cd['date_st_received']
            valuation_object.date_end_received = cd['date_end_received']
            valuation_object.image_1 = cd['img_1']
            valuation_object.image_2 = cd['img_2']
            valuation_object.image_3 = cd['img_3']
            valuation_object.phone = cd['phone']
            valuation_object.email = cd['email']
            valuation_object.contact_person = cd['contact_person']
            if user.is_authenticated:
                valuation_object.owner = user
            valuation_object.save()
            # save unuque url
            object_saved = get_object_or_404(NewOrder, id=valuation_object.id)
            code_forwarding = code_function(object_saved.id)
            object_saved.custom_id = code_function(object_saved.id)
            object_saved.unique_url = request.build_absolute_uri(
                reverse('app:valuation_success', args=[code_forwarding]))
            object_saved.save()
            # send email to admin
            topic = 'Klient prosi o wycene przesyłki | ID: %s | Nazwa: %s | Email: %s | Phone: %s' % \
                    (valuation_object.id, cd['contact_person'], cd['email'], cd['phone'])
            massage = 'Klient prosi o wycene przesyłki | ID: %s | Nazwa: %s | Email: %s | Phone: %s' % \
                      (valuation_object.id, cd['contact_person'], cd['email'], cd['phone'])
            to = ['info@transportuj24.pl', ]
            send_mail(topic, massage, 'info@transportuj24.pl', to)
            # send email to costumer
            topic_costumer = 'Twoja prośba o wycenę przesyłki w kategorii - %s, została pomyślnie dodana' % \
                             (request.session.get('type_product'))
            massage_costumer = 'Zaloguj się do swojego profilu użytkownika i sprawdź aktualny status przesyłki (transportuj24.pl/logowanie/). Twój unikalny link przesyłki to: %s' % \
                               (object_saved.unique_url)
            to_costumer = [cd['email'], ]
            send_mail(topic_costumer, massage_costumer, 'info@transportuj24.pl', to_costumer)
            # redirect next view
            return HttpResponseRedirect(reverse('app:valuation_success', args=[code_forwarding]))
    else:
        form = FirstStepForm()
    context = {'form': form}
    return render(request, 'app/valuation.html', context)


def valuation_success(request, id_code):
    temp = ['', '', '']
    if settings.SSL:
        temp[0] = 'https:'
    else:
        temp[0] = 'http:'

    temp[1] = ''
    temp[2] = request.META['HTTP_HOST']

    host = temp[0] + '/' + temp[1] + '/' + temp[2]
    error_message = ''

    # <========== Query ==========>
    if request.method == 'POST':
        session_id = str(request.POST.get('p24_session_id'))
        session_id = session_id.split('_')[1]

        transaction_obj = get_object_or_404(Przelewy24Transaction, pk=int(session_id))
        transaction_obj.order_id = request.POST.get('p24_order_id')
        transaction_obj.order_id_full = request.POST.get('p24_order_id_full')
        transaction_obj.save()

        confirmed, confirmation_response = p24_verify(request.POST.get('p24_id_sprzedawcy'),
                                                      request.POST.get('p24_session_id'),
                                                      request.POST.get('p24_order_id'),
                                                      request.POST.get('p24_kwota'))

        if not confirmed:
            transaction_obj.status = choices.P24_STATUS_ACCEPTED_NOT_VERIFIED
            transaction_obj.error_code = confirmation_response[2].decode('cp1252')
            transaction_obj.error_description = confirmation_response[3].decode('cp1252')
            error_message = transaction_obj.error_description
            transaction_obj.save()
        else:
            transaction_obj.status = choices.P24_STATUS_ACCEPTED_VERIFIED
            transaction_obj.save()
        transaction_obj.save()

        # send mail to customer and administrator
        subject = "Payment Result"
        message = 'One user paid PLN ' + str(transaction_obj.amount) + ' by przelexy24.'
        url = 'https://transportuj24.pl/admin/dashboard/neworder/' + str(transaction_obj.order.all().first().pk) + '/change/'
        message = message + ' His/Her email is ' + transaction_obj.email + '. Please check this url. ' + url
        send_mail(subject, message, 'info@transportuj24.pl', ['timurkju@gmail.com', 'info@transportuj24.pl'])

    # <========== Query ==========>
    decode_forwarding = decode_function(id_code)
    object = get_object_or_404(NewOrder, id=int(decode_forwarding))
    user = request.user

    order_form = Przelewy24PrepareForm()
    if not object.verified():
        if object.price:
            transaction = Przelewy24Transaction()
            transaction.amount = object.price
            transaction.email = object.email
            transaction.status = choices.P24_STATUS_INITIATED
            transaction.save()

            object.transaction = transaction
            object.save()

            session_id = temp[2] + '_' + str(object.transaction.pk)
            price = int(object.price * 100)

            form_value = {
                'p24_session_id': session_id,
                'p24_id_sprzedawcy': settings.SELLER_ID,
                'p24_email': object.email,
                'p24_kwota': price,
                'p24_opis': '',
                'p24_klient': object.contact_person,
                'p24_adres': '',
                'p24_kod': '',
                'p24_miasto': '',
                'p24_kraj': 'PL',
                'p24_language': 'pl',
                'p24_return_url_ok': host + '/wycena/przesylka-dodana/' + object.custom_id + '/',
                'p24_return_url_error': host + '/wycena/przesylka-dodana/' + object.custom_id + '/',
                'p24_crc': crc_code(session_id, settings.SELLER_ID, price, settings.CRC_KEY),
            }
            order_form = Przelewy24PrepareForm(form_value)

    context = {'user': user,
               'object': object,
               'order_form': order_form,
               'secure': request.is_secure(),
               'error_message': error_message,
               }

    return render(request, 'app/valuation_success.html', context)


def payment_result(request):
    if request.method == 'POST':
        session_id = str(request.POST.get('p24_session_id'))
        session_id = session_id.split('_')[1]

        transaction_obj = get_object_or_404(Przelewy24Transaction, pk=int(session_id))
        transaction_obj.order_id = request.POST.get('p24_order_id')
        transaction_obj.order_id_full = request.POST.get('p24_order_id_full')
        transaction_obj.save()

        confirmed, confirmation_response = p24_verify(request.POST.get('p24_id_sprzedawcy'),
                                                      request.POST.get('p24_session_id'),
                                                      request.POST.get('p24_order_id'),
                                                      request.POST.get('p24_kwota'))

        if not confirmed:
            transaction_obj.status = choices.P24_STATUS_ACCEPTED_NOT_VERIFIED
            transaction_obj.error_code = confirmation_response[2].decode('cp1252')
            transaction_obj.error_description = confirmation_response[3].decode('cp1252')
            error_message = transaction_obj.error_description
            transaction_obj.save()
        else:
            transaction_obj.status = choices.P24_STATUS_ACCEPTED_VERIFIED
            transaction_obj.save()
        transaction_obj.save()

        # send mail to customer and administrator
        subject = "Payment Result"
        message = 'One user paid PLN ' + str(transaction_obj.amount) + ' by przelexy24.'
        url = 'https://transportuj24.pl/admin/dashboard/neworder/' + str(
            transaction_obj.order.all().first().pk) + '/change/'
        message = message + ' His/Her email is ' + transaction_obj.email + '. Please check this url. ' + url
        send_mail(subject, message, 'info@transportuj24.pl', ['timurkju@gmail.com', 'info@transportuj24.pl'])



    return HttpResponseRedirect(reverse('dashboard:products'))


def p24_verify(seller_id, session_id, order_id, amount):
    url = 'https://secure.przelewy24.pl/transakcja.php'
    data = {
        'p24_id_sprzedawcy': seller_id,
        'p24_session_id': session_id,
        'p24_order_id': order_id,
        'p24_kwota': amount,
        'p24_crc': crc_code(session_id, order_id, amount, settings.CRC_KEY)
    }
    response = requests.post(url, data=data)
    confirmation_response = list(response.iter_lines())
    print(response.status_code)
    print(data)
    print(response)
    print(confirmation_response[0])
    print(confirmation_response[1])

    if response.status_code == 200 and confirmation_response[1] == b'TRUE':
        return True, confirmation_response

    return False, confirmation_response


def crc_code(session_id, seller_id, amount, crc_key):
    crc_hash = "%s|%s|%s|%s" % (
        session_id, seller_id,
        amount, crc_key)

    print(crc_hash)
    m = hashlib.md5()
    m.update(crc_hash.encode())
    crc_code = m.hexdigest()
    print(crc_code)
    return crc_code


def signup_company(request):
    return render(request, 'app/signup_company.html')


def signup_company_1(request):
    return render(request, 'app/signup_company_1.html')


def calc_distance(lat1, lon1, lat2, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(float(lon1))
    lon2 = radians(float(lon2))
    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return c * r


def payment(request, id):
    temp = ['', '', '']
    if settings.SSL:
        temp[0] = 'https:'
    else:
        temp[0] = 'http:'

    temp[1] = ''
    temp[2] = request.META['HTTP_HOST']

    host = temp[0] + '/' + temp[1] + '/' + temp[2]
    hostname = request.META['HTTP_HOST']
    object = get_object_or_404(NewOrder, id=id)
    if not object.verified():
        if object.price:
            transaction = Przelewy24Transaction()
            transaction.amount = object.price
            transaction.email = object.email
            transaction.status = choices.P24_STATUS_INITIATED
            transaction.save()

            object.transaction = transaction
            object.save()

            session_id = hostname + '_' + str(object.transaction.pk)
            price = int(object.price * 100)

            form_value = {
                'p24_session_id': session_id,
                'p24_id_sprzedawcy': settings.SELLER_ID,
                'p24_email': object.email,
                'p24_kwota': price,
                'p24_opis': '',
                'p24_klient': object.contact_person,
                'p24_adres': '',
                'p24_kod': '',
                'p24_miasto': '',
                'p24_kraj': 'PL',
                'p24_language': 'pl',
                'p24_return_url_ok': host + '/payment_result/',
                'p24_return_url_error': host + '/payment_result/',
                'p24_crc': crc_code(session_id, settings.SELLER_ID, price, settings.CRC_KEY),
            }

            order_form = Przelewy24PrepareForm(form_value)

            context ={
                'order_form': order_form
            }

            return render(request, 'app/payment_redirect.html', context)

    return HttpResponseRedirect(reverse('dashboard:products'))

