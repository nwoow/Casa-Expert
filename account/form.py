from django import forms
from product.models import CityService


class CityServiceModelForm(forms.ModelForm):

    class Meta:
        model = CityService
        fields =['city_name','category']

        widgets = {
            'city_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }