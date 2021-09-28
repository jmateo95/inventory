from django.shortcuts import redirect, render
from django.contrib import messages
from inventory import products
from .models import ProductType
from .forms import ProductForm

# Create your views here.

def modify(request):
    products = ProductType.objects.all()
    bandera = False
    context = {
        'products':products,
        'bandera':bandera
    }
    return render(request, "form_edit_orders.html", context) 

def modify_order_product(request,id):
    product = ProductType.objects.get(id = id)
    products = ProductType.objects.all()
    if request.method == 'GET':
        context = {
            'products':products,
            'product':product,    
            'bandera':True
        }
    else:
        product.reorderpoint = request.POST.get('reorderpoint')
        product.orderpoint = request.POST.get('orderpoint')
        product.save()
        messages.success(request, "The order point and reorder point were assigned correctly")
        return redirect ('list')
    return render(request,"form_edit_orders.html",context)