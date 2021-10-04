from django import forms
from django.forms import fields
from .models import ProductType, Category, Suplier

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Suplier
        fields = '__all__'