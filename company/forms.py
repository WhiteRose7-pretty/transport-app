from django import forms


class SearchProductForm(forms.Form):
    date_st_send = forms.CharField(max_length=50,
                                   required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                 'data-toggle': 'datetime',
                                                                 'placeholder': 'Wybierz termin od'}))
    date_end_send = forms.CharField(max_length=50,
                                   required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                 'data-toggle': 'datetime',
                                                                 'placeholder': 'Wybierz termin od'}))
    category = forms.CharField(max_length=50,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Wpisz słowo....'}))



class PriceProductForm(forms.Form):
    price = forms.DecimalField(max_digits=20,
                               decimal_places=2,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Podaj cene... (np. 149.99)'}))



class PriceProductFormPartner(forms.Form):
    price = forms.DecimalField(max_digits=20,
                               decimal_places=2,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Podaj cene... (np. 149.99)'}))
    nip = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-prepend',
                                                                       'data-mask': '000-000-00-00',
                                                                       'placeholder': '123-456-78-91'}))