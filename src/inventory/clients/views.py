from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Client
from .forms import ClientForm

# Create your views here.

def modal_register_client(request):
    exist = False
    clients = Client.objects.all()
    if request.method == 'GET':
        context = {
            'success':exist
        }
    else:
        print(request.POST)
        for client  in clients:
            if client.nit == request.POST.get('nit'):
                exist = True
                print (client.nit)
        if exist:
            context = {
                'success':exist,
                'name_client':request.POST.get('name'),
                'last_name_client':request.POST.get('last_name'),
                'address_client':request.POST.get('address'),
                'phone_client':request.POST.get('phone'),
                'nit_repeat':request.POST.get('nit')
            }
        else:
            client = ClientForm(request.POST)
            print(client)
            if client.is_valid():
                client.save()
                messages.success(request, "Cliente \"" + request.POST.get('name') + "\" Agregado")
                return redirect('home')
            else:
                context = {'success':True}
    return render(request,"cashier/client/register_client.html",context)