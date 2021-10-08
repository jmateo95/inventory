from django import forms
from django.forms import fields
from .models import ProductType, Category, Suplier
from django.forms import ModelForm, TextInput, EmailInput
from django.forms.fields import ChoiceField, CharField, IntegerField
from .models import ProductType


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = '__all__'
        # widgets = {
        #     'name': TextInput(attrs={
        #         'title': 'nombre',
        #         'name': 'nombre',
        #         'class': "form-control",
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'Nombre'
        #         })
        # }
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name']= CharField(label="Nombre", required =True) 
        self.fields['orderpoint']= CharField(label="Punto De Reorden", required =False) 
        self.fields['orderquantity']= CharField(label="Cantidad De Reorden", required =False) 
        self.fields['quantity']= CharField(label="Cantidad Existente", required =True) 
        self.fields['category']= CharField(label="Categoria", required =True)  


        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Suplier
        fields = '__all__'


