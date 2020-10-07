from django import forms



class BasicTypeProductForm(forms.Form):
    type_product = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                'placeholder': 'Wybierz kategorię'}))
    location_from = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                                 'placeholder': 'Skąd?'}))
    location_to = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-control-emphasized',
                                                                               'placeholder': 'Dokąd?'}))