from django.shortcuts import redirect, render
from django.contrib import messages
from inventory import products
from .models import Category, ProductType, Suplier, ProductSuplier
from .forms import ProductForm, CategoryForm, SupplierForm, ProductSupplier

# Create your views here.

def modify_order_product(request,id):
    product = ProductType.objects.get(id = id)
    if request.method == 'GET':
        context = {
            'product':product,    
        }
    else:
        product.orderquantity = request.POST.get('reorderpoint')
        product.orderpoint = request.POST.get('orderpoint')
        product.save()
        messages.success(request, "El punto de orden y el de reorden han sido modficados correctamente")
        return redirect ('listproduct')
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


def listproduct(request):
    products=ProductType.objects.all()
    context = {'products': products}
    return render(request, "products/manager/listproducts.html", context)

def list_categories(request):
    categories = Category.objects.all()
    context = {
            'categories':categories
        }
    return render(request, "manager/list_categories.html", context)

def product_suppliers(request,id):
    product = ProductType.objects.get(id = id)
    product_suppliers = Suplier.objects.filter(Suplier_Producttype__producttype=id)
    other_suppliers= Suplier.objects.exclude(id__in = product_suppliers.values('id'))
    if request.method != 'POST':
        
        form = ProductSupplier(other_suppliers=other_suppliers,producttype=id)
        
        
    else:
        form = ProductSupplier(data=request.POST,other_suppliers=other_suppliers,producttype=id)
        
        if form.is_valid():
            form.save()
            messages.info(request, 'El proveedor se enlazo correctamente')
            return redirect("product_suppliers",id=id)
        else:
            messages.info(request, 'No valido')
    context = { 
             'product':product,
             'product_suppliers':product_suppliers,
             'form':form
        #     'other_suppliers':other_suppliers 
            
        }
    return render(request,"manager/product_supliers.html",context)    
     
    #else:
        #product.orderquantity = request.POST.get('reorderpoint')
        #product.orderpoint = request.POST.get('orderpoint')
        #product.save()
        #messages.success(request, "El punto de orden y el de reorden han sido modficados correctamente")
        #return redirect ('listproduct')
    
