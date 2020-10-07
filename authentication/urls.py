from django.urls import path
from . import views
from .views import LogIn, SignUp, PasswordReset, PasswordResetDone


app_name = 'authentication'


urlpatterns = [
    path('', LogIn.as_view(), name='login'),
    path('rejestracja/', SignUp.as_view(), name='signup'),
    path('przypomnienie-hasla/', PasswordReset.as_view(), name='password_reset'),
    path('przypomnienie-hasla/sukces/', PasswordResetDone.as_view(), name='reset_password_done'),
    path('nowa-firma/', views.new_company, name='new_company'),
    path('nowa-firma/pozytywnie-dodana/', views.new_company_success, name='new_company_success'),
]