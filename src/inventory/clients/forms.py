
from django import forms
from django.db.models import fields
from .models import Client
from django.forms.fields import CharField, IntegerField

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ()
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['nit']= CharField(required=True)
        self.fields['name']= CharField(required=True) 
        self.fields['last_name']= CharField(required=False) 
        self.fields['address']=CharField(required=False)
        self.fields['phone']=CharField(required=False)