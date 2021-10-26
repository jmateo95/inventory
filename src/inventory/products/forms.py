from django import forms
from django.forms import fields
from .models import ProductType, Category, Supplier, ProductSupplier
from django.forms import ModelForm, TextInput, EmailInput, ModelChoiceField
from django.forms.fields import ChoiceField, CharField, IntegerField
from .models import ProductType, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductType
        exclude = ('quantity','default_supplier','order_in_progress')
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name']= CharField(label="Nombre", required =True) 
        self.fields['orderpoint']= IntegerField(label="Punto De Reorden", required =False,min_value=0) 
        self.fields['orderquantity']= IntegerField( label="Cantidad De Reorden", required =False,min_value=0)
        self.fields['category']= ModelChoiceField(queryset= Category.objects, label="Categoria", required =True, empty_label='Seleccione una categoria')  

class ProductSupplierForm(forms.ModelForm):
    class Meta:
        model = ProductSupplier
        fields = ('supplier','producttype')
    def __init__(self, *args, **kwargs):
        aux=kwargs.pop('aux')
        if aux==0:
            other_producttypes=kwargs.pop('other_producttypes')
            supplier=kwargs.pop('supplier')
        else:
            producttype=kwargs.pop('producttype')
            other_suppliers=kwargs.pop('other_suppliers')
        
        super(ProductSupplierForm, self).__init__(*args, **kwargs)
        if aux==1:
        
            self.fields['supplier']= ModelChoiceField(queryset=other_suppliers , label="Proveedor", required =True, empty_label='Seleccione un Proveedor')
            self.fields["producttype"].initial=producttype
        else:    
            self.fields['supplier'].initial=supplier
            self.fields["producttype"]= ModelChoiceField(queryset=other_producttypes , label="Producto", required =True, empty_label='Seleccione un Producto')
          
            
              

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

