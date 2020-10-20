from django import forms
from allauth.account.forms import LoginForm, SignupForm
from dashboard.models import CompanyUser
from django.forms import FileInput


class SimpleLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(SimpleLoginForm, self).__init__(*args, **kwargs)
        # change fields
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email',
                                                             'class': 'form-control form-control-prepend',
                                                             'placeholder': 'nazwa@domena.pl'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'type': 'password',
                                                                    'class': 'form-control form-control-prepend',
                                                                    'placeholder': '*************'})



class SimpleSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SimpleSignupForm, self).__init__(*args, **kwargs)
        #change fields
        self.fields['email'].widget = forms.TextInput(attrs={'type': 'email',
                                                             'class': 'form-control form-control-prepend',
                                                             'placeholder': 'nazwa@domena.pl'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'type': 'password',
                                                                     'class': 'form-control form-control-prepend',
                                                                     'placeholder': '*************'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'type': 'password',
                                                                     'class': 'form-control form-control-prepend',
                                                                     'placeholder': '*************'})


class NewCompanyForm(forms.Form):
    company_name = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepend',
                                                                                'placeholder': 'Podaj nazwę firmy...'}))
    location = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepend',
                                                                             'placeholder': 'Podaj firmowy adres...'}))
    company_phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepend',
                                                                                 'data-mask': '(+00) 000 000 000',
                                                                                 'placeholder': '(+48) 505 606 707'}))
    company_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-prepend',
                                                                    'placeholder': 'przyklad@domena.pl',}))
    nip = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepend',
                                                                       'data-mask': '000-00-00-000',
                                                                       'placeholder': '123-45-67-819'}))
    licence = forms.FileField(widget=FileInput(attrs={'class': 'custom-input-file',}))
    contact_person = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepend',
                                                                                  'placeholder': 'Podaj imię osoby kontaktowej...'}))
    directions_supported = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepend',
                                                                                        'placeholder': 'Wpisz jakie kierunki obsługuje Twoja firma...'}))
    vehicle_fleet = forms.CharField(widget=forms.Textarea(attrs={'rows': '3',
                                                                 'class': 'form-control',
                                                                 'placeholder': 'Napisz parę słów jaką flotą pojazdów dysponuje Twoja firma...'}))