from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from dashboard.models import Category, Newsletter, TypeProduct, NewOrder
from django.shortcuts import get_object_or_404
from .forms import BasicTypeProductForm, FirstStepForm
import random
from math import radians, cos, sin, asin, sqrt
from django.http import JsonResponse
from django.core.mail import send_mail
from .additional_functions import code_function, decode_function
from dashboard.forms import ContactPhoneForm, EmailContactForm
from .models import PrivacyPolicy


def home(request):
    #query
    post_list = Newsletter.objects.all()[:9]
    type_products = TypeProduct.objects.all()
    send = request.session.get('send')
    if send:
        request.session['send'] = None

    #form
    if request.method == 'POST' and 'valuationButtonSubmit' in request.POST:
        form = BasicTypeProductForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            distance = calc_distance(form_data['lat_from'], form_data['lng_from'], form_data['lat_to'], form_data['lng_to'])
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
            send_mail(topic, massage, 'benjamin.langeriaf7@gmail.com', to)
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
            send_mail(topic, massage, 'benjamin.langeriaf7@gmail.com', to)
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
            #save unuque url
            object_saved = get_object_or_404(NewOrder, id=valuation_object.id)
            code_forwarding = code_function(object_saved.id)
            object_saved.custom_id = code_function(object_saved.id)
            object_saved.unique_url = request.build_absolute_uri(reverse('app:valuation_success', args=[code_forwarding]))
            object_saved.save()
            #send email to admin
            topic = 'Klient prosi o wycene przesyłki | ID: %s | Nazwa: %s | Email: %s | Phone: %s' % \
                    (valuation_object.id, cd['contact_person'], cd['email'], cd['phone'])
            massage = 'Klient prosi o wycene przesyłki | ID: %s | Nazwa: %s | Email: %s | Phone: %s' % \
                    (valuation_object.id, cd['contact_person'], cd['email'], cd['phone'])
            to = ['info@transportuj24.pl', ]
            send_mail(topic, massage, 'benjamin.langeriaf7@gmail.com', to)
            # send email to costumer
            topic_costumer = 'Twoja prośba o wycenę przesyłki w kategorii - %s, została pomyślnie dodana' % \
                    (request.session.get('type_product'))
            massage_costumer = 'Zaloguj się do swojego profilu użytkownika i sprawdź aktualny status przesyłki (transportuj24.pl/logowanie/). Twój unikalny link przesyłki to: %s' % \
                    (object_saved.unique_url)
            to_costumer = [cd['email'], ]
            send_mail(topic_costumer, massage_costumer, 'benjamin.langeriaf7@gmail.com', to_costumer)
            #redirect next view
            return HttpResponseRedirect(reverse('app:valuation_success', args=[code_forwarding]))
    else:
        form = FirstStepForm()
    context = {'form': form}
    return render(request, 'app/valuation.html', context)


def valuation_success(request, id_code):
    #<========== Query ==========>
    decode_forwarding = decode_function(id_code)
    object = get_object_or_404(NewOrder, id=int(decode_forwarding))
    user = request.user

    context = {'user': user,
               'object': object}
    return render(request, 'app/valuation_success.html', context)



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
    return (c * r)
