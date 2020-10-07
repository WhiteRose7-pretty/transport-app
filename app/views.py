from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from dashboard.models import Category, Newsletter, TypeProduct
from django.shortcuts import get_object_or_404
from .forms import BasicTypeProductForm
import random
from math import radians, cos, sin, asin, sqrt
from django.http import JsonResponse


def home(request):
    #query
    post_list = Newsletter.objects.all()[:9]
    type_products = TypeProduct.objects.all()

    #form
    if request.method == 'POST':
        form = BasicTypeProductForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            distance = calc_distance(form_data['lat_from'], form_data['lng_from'], form_data['lat_to'], form_data['lng_to'])
            request.session['location_from'] = form_data['location_from']
            request.session['location_to'] = form_data['location_to']
            request.session['distance'] = distance
            print(distance)
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

    context = {'post_list': post_list,
               'type_products': type_products,
               'form': form}
    return render(request, 'app/home.html', context)


def login(request):
    return render(request, 'app/login.html')



def signup(request):
    return render(request, 'app/signup.html')



def blog(request):
    post_list = Newsletter.objects.all()
    category = Category.objects.all()
    logo_white = True

    context = {'post_list': post_list,
               'logo_white': logo_white,
               'category': category}
    return render(request, 'app/blog.html', context)



def article(request, id):
    object = get_object_or_404(Newsletter, pk=id)
    try:
        random_article = random.sample(list(Newsletter.objects.exclude(id=object.id)), 3)
    except:
        random_article = None

    context = {'object': object,
               'random_article': random_article}
    return render(request, 'app/article.html', context)



def valuation(request):
    distance = request.session.get('distance')
    context = {
        'distance': distance
    }
    return render(request, 'app/valuation.html', context)


def valuation_second(request):
    return render(request, 'app/valuation_second.html')


def valuation_third(request):
    return render(request, 'app/valuation_third.html')



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
