from django import forms
from django.forms import ModelChoiceField

from inventory.users.models import Rol, User

class UsersForm(forms.ModelForm):
    rol = ModelChoiceField(queryset=Rol.objects.all(),  empty_label='Please select Rol.')
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model= User
        fields= ['email', 'username', 'rol', 'password']
    