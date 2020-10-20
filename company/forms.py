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