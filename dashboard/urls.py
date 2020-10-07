from django.urls import path
from . import views

app_name = 'dashboard'


urlpatterns = [
    path('', views.home, name='home'),
    path('produkty/', views.products, name='products'),
    path('ustawienia-konta/', views.settings, name='settings'),
]