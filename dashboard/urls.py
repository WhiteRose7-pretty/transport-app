from django.urls import path
from . import views

app_name = 'dashboard'


urlpatterns = [
    path('', views.chat, name='chat'),
    path('produkty/', views.products, name='products'),
    path('ustawienia-konta/', views.settings, name='settings'),
    path('kontakt-telefoniczny/', views.phone_contact, name='phone_contact'),
]