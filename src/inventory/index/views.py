from django.shortcuts import render, redirect
import json
from django.contrib import messages

from inventory.index.forms import UsersForm

# Create your views here.


def index(request):
    option=[]
    name=[]
    option.append('{"title": {"text": "ejempo_0"},"xAxis": {"type": "category","data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},"yAxis": {"type": "value"},"series": [{"data": [150, 230, 224, 218, 135, 147, 260],"type": "line","name": "uno"},{"data": [160, 220, 214, 228, 145, 157, 270],"type": "line","name": "dos"}]}')
    option.append('{"title": {"text": "ejempo_1"},"xAxis": {"type": "category","data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},"yAxis": {"type": "value"},"series": [{"data": [150, 230, 224, 218, 135, 147, 260],"type": "line","name": "uno"},{"data": [160, 220, 214, 228, 145, 157, 270],"type": "line","name": "dos"}]}')
    option.append('{"title": {"text": "ejempo_2"},"xAxis": {"type": "category","data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},"yAxis": {"type": "value"},"series": [{"data": [150, 230, 224, 218, 135, 147, 260],"type": "line","name": "uno"},{"data": [160, 220, 214, 228, 145, 157, 270],"type": "line","name": "dos"}]}')
    name.append('id_0')
    name.append('id_1')
    name.append('id_2')
    json_option = json.dumps(option)
    json_name = json.dumps(name)
    nombre='Jonathan'
    #messages.success(request, "Registration successful." )
    form = UsersForm(request.POST or None, request.FILES or None)
    context = {
        'options' :json_option ,
        'names':json_name,
        'nombre': nombre,
        'form' : form,
    }
    if (request.user.rol.id==1):
        return redirect ('dashboard')
    elif(request.user.rol.id==2):
        return redirect ('listproduct')
    else:
        return redirect ('register_sale')

    #return render(request, "index/index.html", context) 


def addgraph(request):
    form = UsersForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        messages.success(request, "Formulario")
        return redirect ('/')
        