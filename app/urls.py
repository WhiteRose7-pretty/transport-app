from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('logowanie/', views.login, name='login'),
    path('rejestracja/', views.signup, name='signup'),
    path('rejestracja/firma/', views.signup_company, name='signup_company'),
    path('rejestracja/firma/1/', views.signup_company_1, name='signup_company_1'),
    path('blog/', views.blog, name='blog'),
    path('artykul/<int:id>/', views.article, name='article'),
    path('wycena/', views.valuation, name='valuation'),
    path('wycena/krok-2/', views.valuation_second, name='valuation_second'),
    path('wycena/krok-3/', views.valuation_third, name='valuation_third'),
]