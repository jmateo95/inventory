from django import forms
from django.forms import fields
from .models import ProductType

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = '__all__'