from django.db.models.aggregates import Sum
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse

from inventory.products.views import automatic_order
from .models import Client, TempProductSale, Sale, ProductSale
from datetime import datetime
from inventory.products.models import GroupProduct,SalePrice,ProductType
from inventory.users.models import User
from .forms import ClientForm
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import *
from django.db import transaction

# Create your views here.

def modal_register_client(request): # Bryan - 1
    exist = False
    clients = Client.objects.all()
    if request.method == 'GET':
        context = {
            'success':exist
        }
    else:
        exist = check_exist_nit(clients, request.POST.get('nit'))
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

def check_exist_nit(clients, compare):
    for client  in clients:
        if client.nit == compare:
            return True
    return False
    
def register_sale(request):
    if request.method == 'GET':
         TempProductSale.objects.all().delete()
    if request.method == 'POST':
        nit=request.POST.get('client_nit')
        if(nit=="C/F" or nit==""):
            client=Client.objects.get(nit="C/F")   
        elif Client.objects.filter(nit = nit).exists():
            client=Client.objects.get(nit = nit)
        else:      
            messages.error(request,'Cliente no existe')
            return render(request,"cashier/register_sale.html") 
        temps=TempProductSale.objects.all()
        if(temps.count()>0):
            user=User.objects.get(username=request.POST.get('user'))
            new_sale=Sale(client=client,cashier=user,datetime=datetime.now(),total=get_temp_total())
            new_sale.save()
            for temp in temps:
                new_product_sale=ProductSale(product=temp.product,sale=new_sale,quantity=temp.quantity,total=temp.total)
                new_product_sale.save()
                remove_products_from_stock(temp.quantity,temp.product)
                if temp.product.producttype.order_in_progress==False:
                    verify_automatic_order(temp.product.producttype)
            messages.info(request, 'Compra Realizada Correctamente')
            TempProductSale.objects.all().delete()    
                
        else:
            messages.error(request,'No existen productos seleccionados')
    groupProduct=GroupProduct.objects.all().order_by("producttype") 
    #print(groupProduct)      
    context={"products":groupProduct}
    return render(request,"cashier/register_sale.html",context)   

def verify_automatic_order(producttype):
    if producttype.quantity<=producttype.orderpoint and producttype.default_supplier != None:
        if automatic_order(producttype):
            producttype.order_in_progress = True
            producttype.save()

@transaction.atomic
def remove_products_from_stock(quantity,productgroup):
    productgroup.quantity=productgroup.quantity-quantity
    productgroup.producttype.quantity=productgroup.producttype.quantity-quantity
    productgroup.save()
    productgroup.producttype.save()

def autocomplete_upc(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        products = get_upc_for_autocomplete(query)
        titles = list()
        for product in products:
            titles.append(str(product.upc))
        data = json.dumps(titles)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

def get_upc_for_autocomplete(term):
    return GroupProduct.objects.filter(upc__icontains=term)

def autocomplete_client(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        clients = get_nit_for_autocomplete(query)
        
        titles = list()
        for product in clients:
            titles.append(product.nit)
        data = json.dumps(titles)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

def get_nit_for_autocomplete(term):
    return Client.objects.filter(nit__icontains=term)

@csrf_exempt
def insert_product(request):
    data=request.POST.get("data")
    upc=request.POST.get("upc")
    quantity=request.POST.get("quantity")
    number=TempProductSale.objects.all().count()+1
    if upc=="" or not upc.isnumeric() or not GroupProduct.objects.filter(upc=upc).exists():
        response_data={"error":True,"errorMessage":"UPC invalido"}
        return JsonResponse(response_data,safe=False)
    group=GroupProduct.objects.get(upc=upc)
    product_name=group.producttype.name
    saleprice=SalePrice.objects.filter(producttype=group.producttype).order_by('-channgeddate').first()
    total=get_total(quantity,saleprice)
    temps=TempProductSale.objects.filter(product=group)
    
    aux=0
    for temp in temps:
        aux+=temp.quantity
        
    if (int(quantity)+aux)>group.quantity:
        response_data={"error":True,"errorMessage":"Cantidad no disponible en inventario"}
        return JsonResponse(response_data,safe=False)
    else:

    #Creates temp model
        tempSale=TempProductSale(number=number,product=group,quantity=quantity,total=total)
        tempSale.save()
        
        temp_total=get_temp_total()
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
    return Decimal(quantity)*Decimal(saleprice.price)

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
    response_data={"error":False,"errorMessage":"Updated Successfully","temp_total":str(get_temp_total())}
    return JsonResponse(response_data,safe=False)

def list_client(request):
    context = { 'clients':Client.objects.all() }
    return render (request, "cashier/client/list-client.html", context)

def transacction_cashier(request):
    transactions = Sale.objects.filter(cashier=request.user).filter(datetime__gte=datetime.today().replace(hour=00).replace(minute=00).replace(second=00))
    total = transactions.aggregate(total_price=Sum('total'))['total_price']
    
    context = {
        'date':datetime.now(),
        'transactions':transactions,
        'total':total
    }
    if request.method == 'POST':
        if request.POST.get('date-time'):
            transactions = Sale.objects.filter(cashier=request.user).filter(datetime__lte=request.POST.get('date-time'))
            total = transactions.aggregate(total_price=Sum('total'))['total_price']
            context = {
                'date':request.POST.get('date-time'),
                'transactions':transactions,
                'total':total
            }
    return render (request, "cashier/list-transactions.html", context)

def transacction(request):
    transactions = Sale.objects.all().filter(datetime__gte=datetime.today().replace(hour=00).replace(minute=00).replace(second=00))
    #print ((transactions[0].cashier))
    total = transactions.aggregate(total_price=Sum('total'))['total_price']
    
    context = {
        'date':datetime.now(),
        'transactions':transactions,
        'total':total
    }
    if request.method == 'POST':
        if request.POST.get('date-time'):
            transactions = Sale.objects.filter(cashier=request.user).filter(datetime__lte=request.POST.get('date-time'))
            total = transactions.aggregate(total_price=Sum('total'))['total_price']
            context = {
                'date':request.POST.get('date-time'),
                'transactions':transactions,
                'total':total
            }
    return render (request, "manager/transactions.html", context)