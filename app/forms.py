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
    date_st_send = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                'data-toggle': 'date',
                                                                                'placeholder': 'Wybierz termin od'}))
    date_end_send = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                'data-toggle': 'date',
                                                                                'placeholder': 'Wybierz termin do'}))
    date_st_received = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                'data-toggle': 'date',
                                                                                'placeholder': 'Wybierz termin od'}))
    date_end_received = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
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

