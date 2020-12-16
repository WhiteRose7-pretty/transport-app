from django import forms
from django.forms import FileInput
from dashboard.models import TypeProduct

CHOICE_TYPE = [
    ('%s'%(i), '%s'%(i)) for i in TypeProduct.objects.all()
]

CHOICE_TYPE_CATEGORY = [
    ('', 'Wybierz kategorię')
] + CHOICE_TYPE

class BasicTypeProductForm(forms.Form):
    type_product = forms.ChoiceField(label='',
                                     choices=CHOICE_TYPE_CATEGORY,
                                     widget=forms.Select(attrs={'class': 'form-control form-control-emphasized'}))
    location_from = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                 'placeholder': 'Skąd?'}))
    location_to = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                               'placeholder': 'Dokąd?'}))

    lat_from = forms.CharField(max_length=500, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                 'placeholder': 'Skąd?'}))
    lng_from = forms.CharField(max_length=500, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                               'placeholder': 'Dokąd?'}))

    lat_to = forms.CharField(max_length=500, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                 'placeholder': 'Skąd?'}))
    lng_to = forms.CharField(max_length=500, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                               'placeholder': 'Dokąd?'}))



class FirstStepForm(forms.Form):
    length = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-emphasized',
                                                                'placeholder': 'Wartość w cm'}))
    width = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-emphasized',
                                                                'placeholder': 'Wartość w cm'}))
    height = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-emphasized',
                                                                'placeholder': 'Wartość w cm'}))
    weight = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-emphasized',
                                                                'placeholder': 'Wartość w kg'}))
    quantity = forms.IntegerField(initial=1, widget=forms.NumberInput(attrs={'class': 'form-control form-control-emphasized',
                                                                  'placeholder': 'Ilość sztuk do przesłania...'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '4',
                                                            'class': 'form-control form-control-emphasized',
                                                            'placeholder': 'Powiedz nam parę słów o swojej przesyłce...'}))
    date_st_send = forms.DateTimeField(label='Czas wysłania od:', widget=forms.DateTimeInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                'data-toggle': 'date',
                                                                                'placeholder': 'Wybierz termin od'}))
    date_end_send = forms.DateTimeField(label='Czas wysłania do:', required=False, widget=forms.DateTimeInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                'data-toggle': 'date',
                                                                                'placeholder': 'Wybierz termin do'}))
    date_st_received = forms.DateTimeField(label='Czas odbioru od:', required=False, widget=forms.DateTimeInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                'data-toggle': 'date',
                                                                                'placeholder': 'Wybierz termin od'}))
    date_end_received = forms.DateTimeField(label='Czas odbioru do:', required=False, widget=forms.DateTimeInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                'data-toggle': 'date',
                                                                                'placeholder': 'Wybierz termin do'}))
    img_1 = forms.ImageField(required=False, widget=FileInput(attrs={'class': 'custom-input-file',
                                                   'accept': '.jpg, .jpeg, .png',}))
    img_2 = forms.ImageField(required=False, widget=FileInput(attrs={'class': 'custom-input-file',
                                                   'accept': '.jpg, .jpeg, .png',}))
    img_3 = forms.ImageField(required=False, widget=FileInput(attrs={'class': 'custom-input-file',
                                                   'accept': '.jpg, .jpeg, .png',}))
    phone = forms.CharField(max_length=30,
                            initial='48 ',
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                         'data-mask': '(+00) 000-000-000',
                                                                         'placeholder': '(+00) 000 000 000'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-emphasized',
                                                            'placeholder': 'nazwa@domena.pl',}))
    contact_person = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                  'placeholder': 'Podaj tekst...'}))


class Przelewy24PrepareForm(forms.Form):
    p24_session_id = forms.CharField(max_length=100, label='', widget=forms.HiddenInput())
    p24_id_sprzedawcy = forms.CharField(max_length=100, label='', widget=forms.HiddenInput())
    p24_email = forms.CharField(max_length=100, label='email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    p24_kwota = forms.CharField(max_length=100, label='', widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    # p24_opis = forms.CharField(max_length=100, label='title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    p24_klient = forms.CharField(max_length=100, label='surname', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # p24_adres = forms.CharField(max_length=100, label='address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # p24_kod = forms.CharField(max_length=100, label='zip code', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # p24_miasto = forms.CharField(max_length=100, label='city', widget=forms.TextInput(attrs={'class': 'form-control'}))
    p24_kraj = forms.CharField(max_length=100, label='', widget=forms.HiddenInput())
    p24_language = forms.CharField(max_length=100, label='', widget=forms.HiddenInput())
    p24_return_url_ok = forms.CharField(max_length=100, label='', widget=forms.HiddenInput())
    p24_return_url_error = forms.CharField(max_length=100, label='', widget=forms.HiddenInput())
    p24_crc = forms.CharField(max_length=100, label='', widget=forms.HiddenInput())

