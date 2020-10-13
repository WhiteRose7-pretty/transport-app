from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('polityka-prywatnosci/', views.privacy_policy, name='privacy_policy'),
    path('regulamin-strony/', views.terms, name='terms'),
    path('rejestracja/firma/', views.signup_company, name='signup_company'),
    path('rejestracja/firma/1/', views.signup_company_1, name='signup_company_1'),
    path('blog/', views.blog, name='blog'),
    path('artykul/<int:id>/', views.article, name='article'),
    path('wycena/', views.valuation, name='valuation'),
    path('wycena/przesylka-dodana/<id_code>/', views.valuation_success, name='valuation_success'),
]