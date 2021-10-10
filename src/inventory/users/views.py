from django.shortcuts import render, redirect
import json
from django.contrib import messages
from inventory.users.forms import UsersForm
from django.http.response import HttpResponseRedirect
from inventory.users.models import Rol, User
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


def edituser(request,id):
    user=User.objects.filter(id=id).first()
    roles=Rol.objects.all()

    if(user):
        if request.method == 'GET':
            context = {
                'user':user,
                'roles':roles
            }
            return render(request, "administrator/edituser.html", context)        
        else:
            try:
                user.email = request.POST.get('email')
                user.username = request.POST.get('username')
                user.rol_id= request.POST.get('rol')
                user.save()
                messages.success(request, "El Usuario se modifico correctamente")
                return redirect ('listuser')
            except:
                messages.error(request, "Correo o User Name ya existentes")
                return redirect ('listuser')
    else:
        messages.error(request, "El usuario no existe" )
        return redirect ('listuser')