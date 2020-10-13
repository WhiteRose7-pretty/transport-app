from django.shortcuts import render
from dashboard.models import NewOrder



def products(request):
    nav_activate = 2
    user_products = NewOrder.objects.all().order_by('-updated_at')

    context ={'nav_activate': nav_activate,
              'user_products': user_products}
    return render(request, 'company/products.html', context)



def chat(request):
    nav_activate = 1

    context = {'nav_activate': nav_activate}
    return render(request, 'company/chat.html', context)