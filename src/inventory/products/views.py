from django.shortcuts import redirect, render
from django.contrib import messages
from inventory import products
from .models import Category, ProductType, Suplier
from .forms import ProductForm, CategoryForm, SupplierForm

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

def create_supplier(request):
    exist = False
    suppliers = Suplier.objects.all()
    if request.method == 'GET':
        context = {
            'success':exist
        }
    else:
        for supplier  in suppliers:
            if supplier.email.lower() == request.POST.get('email').lower():
                exist = True
                print (supplier.email.lower())
        if exist:
            context = {
                'success':exist,
                'name_supplier':request.POST.get('name'),
                'address_supplier':request.POST.get('address'),
                'phone_supplier':request.POST.get('phone'),
                'email_repeat':request.POST.get('email')
            }
        else:
            supplier = SupplierForm(request.POST)
            if supplier.is_valid():
                supplier.save()
                messages.success(request, "Proveedor \"" + request.POST.get('name') + "\" Agregado")
                return redirect('home')
    return render(request,"manager/form_create_supplier.html",context)


def create_product_type(request):
    """Create a product type"""
    if request.method != 'POST':
        #No data submitted
        form = ProductForm()
    else:
        #POST data submitted
        if "cancel" in request.POST:
            return redirect("/")
        else:
            form = ProductForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, 'El tipo de producto se creo correctamente!!')
                return redirect("/") 
    context = {'form': form}        
    return render(request, "manager/create_product_type.html", context) 
