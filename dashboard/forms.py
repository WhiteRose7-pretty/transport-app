from django import forms



class EditAccountBasicInformation(forms.Form):
    profile_img = forms.ImageField(required=False,
                                   widget=forms.FileInput(attrs={'class': 'd-none',
                                                           'accept': '.jpg, .jpeg', }))
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Podaj imie'}))
    surname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Podaj naziwsko'}))


class EditPasswordForm(forms.Form):
    lastpassword = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Aktualne hasło'}))
    newpassword1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Nowe hasło'}))
    newpassword2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Powtórz hasło'}))


class EditCompanyDataForm(forms.Form):
    PROVINCES_CHOICES = [
        ('Mazowieckie', 'Mazowieckie'),
        ('Śląskie', 'Śląskie'),
        ('Wielkopolskie', 'Wielkopolskie'),
        ('Małopolskie', 'Małopolskie'),
        ('Dolnośląskie', 'Dolnośląskie'),
        ('Łódzkie', 'Łódzkie'),
        ('Pomorskie', 'Pomorskie'),
        ('Podkarpackie', 'Podkarpackie'),
        ('Lubelskie', 'Lubelskie'),
        ('Kujawsko-pomorskie', 'Kujawsko-pomorskie'),
        ('Zachodniopomorskie', 'Zachodniopomorskie'),
        ('Warmińsko-mazurskie', 'Warmińsko-mazurskie'),
        ('Świętokrzyskie', 'Świętokrzyskie'),
        ('Podlaskie', 'Podlaskie'),
        ('Lubuskie', 'Lubuskie'),
        ('Opolskie', 'Opolskie'),
    ]
    company_name = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Podaj nazwę firmy'}))
    nip = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'Podaj NIP'}))
    province = forms.ChoiceField(choices=PROVINCES_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Podaj miasto'}))
    zip_code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': '00-000'}))
    street = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Podaj ulice i numer domu'}))


class ContactPhoneForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Podaj imię lub firmę...'}))
    phone = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Podaj numer telefonu...'}))
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'data-mask': '0000-00-00 00:00',
                                                         'placeholder': 'RRRR-MM-DD HH:MM'
                                                         }))


class EmailContactForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Podaj adres email...',}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '6',
                                                               'class': 'form-control',
                                                               'placeholder': 'Wpisz treść wiadomości...'}))