from django.shortcuts import redirect, render
from django.contrib import messages
from inventory import products
from .models import Category, ProductType
from .forms import ProductForm, CategoryForm

# Create your views here.

def modify(request):
    products = ProductType.objects.all()
    bandera = False
    context = {
        'products':products,
        'bandera':bandera
    }
    return render(request, "manager/form_edit_orders.html", context) 

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
        messages.success(request, "El punto de orden y el de reorden han sido modficados correctamente")
        return redirect ('list')
    return render(request,"manager/form_edit_orders.html",context)

def create_category(request):
    categories = Category.objects.all()
    exist = False
    if request.method == 'GET':
        context = {
            'categories':categories
        }
    else:
        for category in categories:
            if category.name.lower() == request.POST.get('name').lower():
                exist = True
        if exist:
            context = {
                'success':exist,
                'categories':categories,
                'name_category':request.POST.get('name')
            }
        else:
            category = CategoryForm(request.POST)
            if category.is_valid():
                category.save()
                messages.success(request, "Categoria \"" + request.POST.get('name') + "\" Agregada")
                return redirect('home')
    return render(request,"manager/form_create_category.html", context)