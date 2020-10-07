from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from dashboard.models import Category, Newsletter, TypeProduct
from django.shortcuts import get_object_or_404
from .forms import BasicTypeProductForm
import random


def home(request):
    #query
    post_list = Newsletter.objects.all()[:9]
    type_products = TypeProduct.objects.all()

    #form
    if request.method == 'POST':
        form = BasicTypeProductForm(request.POST)
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
    return render(request, 'app/valuation.html')


def valuation_second(request):
    return render(request, 'app/valuation_second.html')


def valuation_third(request):
    return render(request, 'app/valuation_third.html')



def signup_company(request):
    return render(request, 'app/signup_company.html')



def signup_company_1(request):
    return render(request, 'app/signup_company_1.html')
