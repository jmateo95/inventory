from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from .models import Client, TempProductSale, Sale, ProductSale
from datetime import datetime
from inventory.products.models import GroupProduct,SalePrice,ProductType
from inventory.users.models import User
from .forms import ClientForm
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import *

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
    if request.method == 'GET':
         TempProductSale.objects.all().delete()
    if request.method == 'POST':
        nit=request.POST.get('client_nit')
        
        if(nit=="C/F" or nit==""):
            client=Client.objects.get(nit="C/F")   
        elif Client.objects.filter(nit = nit).exists():
            client=Client.objects.filter(nit = nit)
        else:      
            messages.error(request,'Cliente no existe')
        temps=TempProductSale.objects.all()
        if(temps.count()>0):
            user=User.objects.get(username=request.POST.get('user'))
            new_sale=Sale(client=client,cashier=user,datetime=datetime.now(),total=get_temp_total(TempProductSale.objects.all()))
            new_sale.save()
            for temp in temps:
                new_product_sale=ProductSale(product=temp.product,sale=new_sale,quantity=temp.quantity,total=temp.total)
                new_product_sale.save()
                messages.info(request, 'Compra Realizada Correctamente')
                TempProductSale.objects.all().delete()
        else:
            messages.error(request,'No existen productos seleccionados')
            
    context={}
    return render(request,"cashier/register_sale.html",context)   

def autocomplete_upc(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        products = GroupProduct.objects.filter(upc__icontains=query)
        titles = list()
        for product in products:
            titles.append(str(product.upc))
        data = json.dumps(titles)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

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


@csrf_exempt
def insert_product(request):
    data=request.POST.get("data")
    upc=request.POST.get("upc")
    quantity=request.POST.get("quantity")
    number=TempProductSale.objects.all().count()+1
    group=GroupProduct.objects.get(upc=upc)
    product_name=group.producttype.name
    total=get_total(quantity,SalePrice.objects.filter(producttype=group.producttype).order_by('-channgeddate').first())
    #Creates temp model
    tempSale=TempProductSale(number=number,product=group,quantity=quantity,total=total)
    tempSale.save()
    temp_total=get_temp_total(TempProductSale.objects.all())
    try:
        productsale={"upc":upc,
                        "quantity":quantity,
                        "saleprice":str(saleprice.price),
                        "product_name":product_name,
                        "number":str(number),
                        "total":total}
        response_data={"productsale": productsale,"error":False,"errorMessage":"Updated Successfully","temp_total":str(temp_total)}
        return JsonResponse(response_data,safe=False)
    except:
        response_data={"error":True,"errorMessage":"Failed to Update Data"}
        return JsonResponse(response_data,safe=False)

def get_total(quantity, saleprice):
    return Decimal(quantity)*saleprice

def get_temp_total():
    total=0
    temps=TempProductSale.objects.all()
    for temp in temps:
        total+=temp.total
    return total


@csrf_exempt
def search_client(request):
    client_nit=request.POST.get("client_nit")
    if Client.objects.filter(nit = client_nit).exists():
        client=Client.objects.get(nit = client_nit)
        clientInfo={"name":str(client),
                        "phone":client.phone}
        try:
            response_data={"clientInfo": clientInfo,"error":False,"errorMessage":"Updated Successfully"}
            return JsonResponse(response_data,safe=False)
        except:
            response_data={"error":True,"errorMessage":"Failed to Update Data"}
            return JsonResponse(response_data,safe=False)
    else:
        try:
            response_data={"error":True,"errorMessage":"Cliente no existe"}
            return JsonResponse(response_data,safe=False)
        except:
            response_data={"error":True,"errorMessage":"Failed to get Client info"}
            return JsonResponse(response_data,safe=False)

@csrf_exempt
def delete_temp_product(request):
    data=request.POST.get("number")
    product_number=data
    temp=TempProductSale.objects.get(number=product_number)
    temp.delete()
    response_data={"error":False,"errorMessage":"Updated Successfully","temp_total":str(get_temp_total(TempProductSale.objects.all()))}
    return JsonResponse(response_data,safe=False)