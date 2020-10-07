from django.urls import path
from . import views

app_name = 'company'


urlpatterns = [
    path('', views.home, name='home'),
    path('produkt/', views.product, name='product'),
    path('ustawienia-konta/', views.settings, name='settings'),
    path('czat/', views.chat, name='chat'),
]