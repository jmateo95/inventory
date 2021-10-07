from django.shortcuts import render, redirect
import json
from django.contrib import messages
from inventory.users.forms import UsersForm
from django.http.response import HttpResponseRedirect
from inventory.users.models import User
from django.contrib.auth.hashers import make_password
from allauth.account.models import EmailAddress
# Create your views here.

def adduser(request):
    form = UsersForm(request.POST or None, request.FILES or None)
    context = {
        'form' : form,
    }
    return render(request, "administrator/adduser.html", context)

def newuser(request):
    form = UsersForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.password=make_password(instance.password)
        instance.is_superuser=False
        instance.is_staff=False
        instance.is_active=True
        instance.save()
        emailAddress=EmailAddress.objects.create(email=instance.email, verified=False, primary=True, user=instance)
        emailAddress.save()
        emailAddress.send_confirmation()
        messages.success(request, "Se envio un correo al nuevo usuario.")
    else:
        messages.error(request, "Ya existe un usuario con el correo o username.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def listuser(request):
    users=User.objects.filter(is_active=True)
    context = {
        'users' : users,
    }
    return render(request, "administrator/listuser.html", context)


def deleteuser(request,id):
    user=User.objects.filter(id=id).first()
    if(user):
        user.is_active=False
        user.save()
        messages.success(request, "Usuario: "+user.email+" eliminado exitosamente" )
    return redirect ('listuser')