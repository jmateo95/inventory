from django import forms
from django.forms import fields
from .models import ProductType, Category, Suplier
from django.forms import ModelForm, TextInput, EmailInput, ModelChoiceField
from django.forms.fields import ChoiceField, CharField, IntegerField
from .models import ProductType, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductType
        exclude = ('quantity',)
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
        self.fields['orderpoint']= IntegerField(label="Punto De Reorden", required =False,min_value=0) 
        self.fields['orderquantity']= IntegerField( label="Cantidad De Reorden", required =False,min_value=0)
        self.fields['category']= ModelChoiceField(queryset= Category.objects, label="Categoria", required =True, placeholder='Seleccione una categoria')  


        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Suplier
        fields = '__all__'


