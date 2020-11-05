from django.shortcuts import render
from allauth.account.views import LoginView, SignupView, PasswordResetView, PasswordResetDoneView
from django.urls import reverse_lazy
from .forms import NewCompanyForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from dashboard.models import CompanyUser
from django.core.mail import send_mail


class LogIn(LoginView):
    template_name = 'authentication/login.html'



class SignUp(SignupView):
    template_name = 'authentication/signup.html'



class PasswordReset(PasswordResetView):
    success_url = reverse_lazy('authentication:reset_password_done')
    template_name = 'authentication/account_reset_password.html'



class PasswordResetDone(PasswordResetDoneView):
    template_name = 'authentication/account_reset_password_done.html'



def new_company(request):
    if request.method == 'POST':
        form = NewCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            company = CompanyUser()
            company.company_name = cd['company_name']
            company.company_phone = cd['company_phone']
            company.company_email = cd['company_email']
            company.nip = cd['nip']
            company.location = cd['location']
            company.licence = cd['licence']
            company.contact_person = cd['contact_person']
            company.directions_supported = cd['directions_supported']
            company.vehicle_fleet = cd['vehicle_fleet']
            company.save()
            topic = 'W serwisie Transportuj24.pl została dodana nowa firma.'
            massage = 'Nowa firma w Transportuj24.pl - %s | http://transportuj24.pl/admin/dashboard/companyuser/' % (cd['company_name'])
            topic_company = 'Witaj w serwisie Transportuj24.pl'
            massage_company = 'Twoja firma została pomyślnie dodana w naszym serwisie transportuj24.pl. Będziemy Cię informować o nowych przesyłkach które możesz wycenić. Jeżeli chcesz się wyrejestrować skontaktuj się z naszym zespołem pod adresem email: info@transportuj24.pl.'
            to = ['info@transportuj24.pl', ]
            send_mail(topic, massage, 'benjamin.langeriaf7@gmail.com', to)
            to_company = [cd['company_email'], ]
            send_mail(topic_company, massage_company, 'benjamin.langeriaf7@gmail.com', to_company)
            return HttpResponseRedirect(reverse('authentication:new_company_success'))
    else:
        form = NewCompanyForm()

    context = {'form': form}
    return render(request, 'authentication/new_company.html', context)



def new_company_success(request):
    return render(request, 'authentication/new_company_success.html')

