from django.shortcuts import render
from .forms import EditAccountBasicInformation, EditPasswordForm, EditCompanyDataForm
from authentication.models import UserHelpedElement, CompanyUserData
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password


def home(request):
    return render(request, 'dashboard/home.html')


def products(request):
    return render(request, 'dashboard/products.html')


def settings(request):
    #basic information
    basic_user_data = UserHelpedElement.objects.filter(owner=request.user).last()
    company_data_object = CompanyUserData.objects.filter(owner=request.user).last()
    send = request.session.get('send')
    if send:
        request.session['send'] = None
    send_error = request.session.get('send_error')
    if send_error:
        request.session['send_error'] = None

    #edit user data
    if request.method == 'POST' and 'buttonAccount' in request.POST:
        form_user_data = EditAccountBasicInformation(request.POST)
        if form_user_data.is_valid():
            cd = form_user_data.cleaned_data
            object = UserHelpedElement()
            object.owner = request.user
            object.name = cd['name']
            object.surname = cd['surname']
            object.save()
            request.session['send'] = 'Twoje informacje o koncie zostały pomyślnie zapisane.'
            return HttpResponseRedirect(reverse('dashboard:settings'))
    else:
        if basic_user_data:
            form_user_data = EditAccountBasicInformation(initial={'name': basic_user_data.name,
                                                                  'surname': basic_user_data.surname})
        else:
            form_user_data = EditAccountBasicInformation()

    #change password
    if request.method == 'POST' and 'buttonPasswordChange' in request.POST:
        security_form = EditPasswordForm(request.POST)
        if security_form.is_valid():
            currentpassword = request.user.password
            currentpasswordentered = security_form.cleaned_data.get('lastpassword')
            password1 = security_form.cleaned_data.get('newpassword1')
            password2 = security_form.cleaned_data.get('newpassword2')
            matchcheck = check_password(currentpasswordentered, currentpassword)
            if matchcheck and password1 == password2:
                user = request.user
                user.set_password(password1)
                user.save()
                request.session['send'] = 'Twoje hasło zostało pomyślnie zmienione.'
                return HttpResponseRedirect(reverse('dashboard:settings'))
            else:
                request.session['send_error'] = 'Wprowadzone przez Ciebie dane nie są poprawne. Spróbój ponownie.'
                return HttpResponseRedirect(reverse('dashboard:settings'))

    else:
        security_form = EditPasswordForm()

    #edit company
    if request.method == 'POST' and 'buttonAdditionalInformation':
        form_company_data = EditCompanyDataForm(request.POST)
        if form_company_data.is_valid():
            cd = form_company_data.cleaned_data
            object = CompanyUserData()
            object.owner = request.user
            object.company_name = cd['company_name']
            object.nip = cd['nip']
            object.province = cd['province']
            object.city = cd['city']
            object.zip_code = cd['zip_code']
            object.street = cd['street']
            object.save()
            request.session['send'] = 'Twoje dane o firmie zostały pomyślnie zapisane.'
            return HttpResponseRedirect(reverse('dashboard:settings'))
    else:
        if company_data_object:
            form_company_data = EditCompanyDataForm(initial={'company_name': company_data_object.company_name,
                                                             'nip': company_data_object.nip,
                                                             'province': company_data_object.province,
                                                             'city': company_data_object.city,
                                                             'zip_code': company_data_object.zip_code,
                                                             'street': company_data_object.street})
        else:
            form_company_data = EditCompanyDataForm()


    context = {'form_user_data': form_user_data,
               'form_company_data': form_company_data,
               'security_form': security_form,
               'send_error': send_error,
               'send': send}
    return render(request, 'dashboard/settings.html', context)