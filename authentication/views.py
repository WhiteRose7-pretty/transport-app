from django.shortcuts import render
from allauth.account.views import LoginView, SignupView, PasswordResetView, PasswordResetDoneView
from django.urls import reverse_lazy
from .forms import NewCompanyForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from dashboard.models import CompanyUser



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
            return HttpResponseRedirect(reverse('authentication:new_company_success'))
    else:
        form = NewCompanyForm()

    context = {'form': form}
    return render(request, 'authentication/new_company.html', context)



def new_company_success(request):
    return render(request, 'authentication/new_company_success.html')

