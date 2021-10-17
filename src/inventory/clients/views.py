from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from .models import Client
from .forms import ClientForm
import json
from django.http import HttpResponse

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
            if client.is_valid():
                client.save()
                messages.success(request, "Cliente \"" + request.POST.get('name') + "\" Agregado")
                return redirect('home')
            else:
                context = {'success':True}
    return render(request,"cashier/client/register_client.html",context)

def register_sale(request):
    # supplier = Supplier.objects.get(id = id,active=True)
    # supplier_products = ProductType.objects.filter(Producttype_Supplier__supplier=id)
    # other_producttypes= ProductType.objects.exclude(id__in = supplier_products.values('id'))
    # aux=0
    # if request.method != 'POST':
        
    #     form = ProductSupplierForm(other_producttypes=other_producttypes,supplier=id,aux=aux)   
    # else:
    #     form = ProductSupplierForm(data=request.POST,other_producttypes=other_producttypes,supplier=id,aux=aux)
        
    #     if form.is_valid():
    #         form.save()
    #         messages.info(request, 'El producto se enlazo correctamente')
    #         return redirect("supplier_products",id=id)
    #     else:
    #         messages.info(request, 'No valido')
    # context = { 
    #          'supplier':supplier,
    #          'supplier_products':supplier_products,
    #          'form':form
            
    #     }
    context={}
    return render(request,"cashier/register_sale.html",context)   


def autocomplete_client(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        clients = Client.objects.filter(nit__icontains=query)
        titles = list()
        for product in clients:
            titles.append(product.nit)
        data = json.dumps(titles)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)
