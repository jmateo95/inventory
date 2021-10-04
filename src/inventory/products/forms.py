from django import forms
from django.forms import fields
from .models import ProductType, Category, Suplier
from django.forms import ModelForm, TextInput, EmailInput
from .models import ProductType


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = {
            "name": "Nombres",
            "orderpoint": "Punto de reorden",
            "orderquantity": "Cantidad de reorden",
            "quantity": "Cantidad Existente",
            "category": "Categoria"
            }
        widgets = {
            'name': TextInput(attrs={
                'title': 'nombre',
                'name': 'nombre',
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Nombre'
                })
        }
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['orderpoint'].required = False 
        self.fields['orderquantity'].required = False 
        self.fields['name']= TextInput(label="Nombre", required =True)  


        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Suplier
        fields = '__all__'


