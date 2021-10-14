from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from inventory import products
from .models import Category, ProductType, Supplier, ProductSupplier
from .forms import ProductForm, CategoryForm, SupplierForm, ProductSupplierForm
from django.http import HttpResponseRedirect

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


def manual_purchase(request,id):
    try:
        product = ProductType.objects.get(id = id)
        if request.method == 'GET':
            suppliers=Supplier.objects.filter(Supplier_Producttype__producttype=product)
            context = {
                'suppliers':suppliers,
                'product':product,    
            }
        else:
            if(int(request.POST.get('quantity')) > 0):
                newproduct=GroupProduct.objects.create(ingressdate=datetime.now(), expirationdate=request.POST.get('expirationdate'), quantity=int(request.POST.get('quantity')), supplier_id=request.POST.get('supplier'))
                newproduct.save()
                product.quantity=product.quantity+newproduct.quantity
                product.save()
                messages.success(request, "Se ingreso la cantidad correctamente")
            else:
                messages.error(request, "Existio un error en la cantidad por favor intentelo de nuevo")
            return redirect ('listproduct')
        return render(request,"products/manager/manual_purchase.html",context)
    except:
        messages.error(request, "El producto seleccionado no existe")
        return redirect('listproduct')





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
    suppliers = Supplier.objects.all()
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
    product_suppliers = Supplier.objects.filter(Supplier_Producttype__producttype=id)
    other_suppliers= Supplier.objects.exclude(id__in = product_suppliers.values('id'))
    aux=1
    if request.method != 'POST':
        form = ProductSupplierForm(other_suppliers=other_suppliers,producttype=id,aux=aux)

    else:
        form = ProductSupplierForm(data=request.POST,other_suppliers=other_suppliers,producttype=id,aux=aux)
        
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
            
        }
    return render(request,"manager/product_suppliers.html",context)    
     

def suppliers(request):
    suppliers = Supplier.objects.all()
    context = {
            'suppliers':suppliers
        }
    return render(request, "manager/suppliers.html", context)   

def deletesupplier(request,id):
    supplier=Supplier.objects.filter(id=id).first()
    if(supplier):
        name = supplier.name
        supplier.delete()
        messages.success(request, "Proveedor "+name+" eliminado exitosamente" )
    return redirect ('suppliers')

def deleteproductsupplier(request,id,id2):
    productsupplier=ProductSupplier.objects.filter(supplier=id,producttype=id2)
    if(productsupplier):
        productsupplier.delete()
        messages.success(request, "Enlace eliminado exitosamente" )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def supplier_products(request,id):
    supplier = Supplier.objects.get(id = id)
    supplier_products = ProductType.objects.filter(Producttype_Supplier__supplier=id)
    other_producttypes= ProductType.objects.exclude(id__in = supplier_products.values('id'))
    aux=0
    if request.method != 'POST':
        
        form = ProductSupplierForm(other_producttypes=other_producttypes,supplier=id,aux=aux)   
    else:
        form = ProductSupplierForm(data=request.POST,other_producttypes=other_producttypes,supplier=id,aux=aux)
        
        if form.is_valid():
            form.save()
            messages.info(request, 'El producto se enlazo correctamente')
            return redirect("supplier_products",id=id)
        else:
            messages.info(request, 'No valido')
    context = { 
             'supplier':supplier,
             'supplier_products':supplier_products,
             'form':form
            
        }
    return render(request,"manager/supplier_products.html",context)   
