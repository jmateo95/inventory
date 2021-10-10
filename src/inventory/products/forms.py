from django import forms
from django.forms import fields
from .models import ProductType, Category, Supplier, ProductSupplier
from django.forms import ModelForm, TextInput, EmailInput, ModelChoiceField
from django.forms.fields import ChoiceField, CharField, IntegerField
from .models import ProductType, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductType
        exclude = ('quantity',)
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name']= CharField(label="Nombre", required =True) 
        self.fields['orderpoint']= IntegerField(label="Punto De Reorden", required =False,min_value=0) 
        self.fields['orderquantity']= IntegerField( label="Cantidad De Reorden", required =False,min_value=0)
        self.fields['category']= ModelChoiceField(queryset= Category.objects, label="Categoria", required =True, empty_label='Seleccione una categoria')  

class ProductSupplier(forms.ModelForm):
    class Meta:
        model = ProductSupplier
        fields = ('supplier','producttype')
    def __init__(self, *args, **kwargs):
        other_suppliers=kwargs.pop('other_suppliers')
        producttype=kwargs.pop('producttype')
        super(ProductSupplier, self).__init__(*args, **kwargs)
        self.fields['supplier']= ModelChoiceField(queryset=other_suppliers , label="Proveedor", required =True, empty_label='Seleccione un Proveedor')
        self.fields["producttype"].initial=producttype
            
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


