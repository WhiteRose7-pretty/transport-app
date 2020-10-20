from django.urls import path
from . import views


app_name = 'company'


urlpatterns = [
    path('', views.products, name='products'),
    path('szczegoly-produktu/<int:id>/', views.product_detail, name='product_detail'),
    path('masowe-wiadomosci/', views.mass_message, name='mass_message'),
    path('czat/', views.chat, name='chat'),
    path('chat/<str:room_name>/', views.chat0, name='chat0'),
]