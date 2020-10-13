from django.urls import path
from . import views


app_name = 'company'


urlpatterns = [
    path('', views.products, name='products'),
    path('czat/', views.chat, name='chat'),
]