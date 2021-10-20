from django import template
from datetime import datetime
from django.db.models import manager
from django.shortcuts import redirect, render
from django.contrib import messages
from inventory import products
from .models import Category, GroupProduct, ProductType, Supplier, ProductSupplier, Order, Order_Products
from .forms import ProductForm, CategoryForm, SupplierForm, ProductSupplierForm
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, message
from django.conf import settings
from django.http import HttpResponseRedirect
import uuid

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
                newproduct=GroupProduct.objects.create(ingressdate=datetime.now(), expirationdate=request.POST.get('expirationdate'), quantity=int(request.POST.get('quantity')), supplier_id=request.POST.get('supplier'), producttype_id=id)
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
                supplier = Supplier.objects.order_by('-id')[0]
                supplier.active = True
                supplier.save()
                messages.success(request, "Proveedor \"" + request.POST.get('name') + "\" Agregado")
                return redirect('suppliers')
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


def listlot(request, id):
    productsg=GroupProduct.objects.filter(producttype_id=id, quantity__gt=0)
    product=ProductType.objects.get(id=id)

    if request.method == 'POST':
        updatelote=GroupProduct.objects.get(upc=request.POST.get('upc'))
        oldquantity=updatelote.quantity
        newquantity=int(request.POST.get('quantity'))
        product.quantity=product.quantity-oldquantity+newquantity
        updatelote.quantity=int(request.POST.get('quantity'))
        updatelote.save()
        product.save()
        messages.success(request, 'La cantidad del lote se actualizo')
    context = {
        'product': product,
        'productsg': productsg,
        }
    return render(request, "products/manager/listlot.html", context)


def list_categories(request):
    categories = Category.objects.all()
    context = {
            'categories':categories
        }
    return render(request, "manager/list_categories.html", context)

def product_suppliers(request,id):
    product = ProductType.objects.get(id = id)
    product_suppliers = Supplier.objects.filter(Supplier_Producttype__producttype=id,active=True)
    other_suppliers= Supplier.objects.exclude(id__in = product_suppliers.values('id')).filter(active=True)
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
    
def list_products_supplier(request, id):
    supplier = Supplier.objects.get(id=id,active=True)
    product_suppliers = ProductType.objects.filter(Producttype_Supplier__supplier=id)
    if(request.method == 'GET'):
        order = Order()
        order.supplier = supplier
        order.validation_key = uuid.uuid4()
        order.save()
        order = Order.objects.order_by('-id')[0]
        request.session['id_order']=order.id
        context = {
            'products':product_suppliers,
            'supplier':supplier,
            'order_id':order.id
        }
    else:
        order = Order.objects.get(id=request.session['id_order'])
        if(int(request.POST.get('quantity')) <= 0):
            messages.error(request,'Debes de ingresar un numero mayor a 0')
        else:
            if (request.POST.get('id_product')):
                product = ProductType.objects.get(id=request.POST.get('id_product'))
                order_product = Order_Products.objects.filter(numberoforder_id=order.id).filter(producttype_id=product.id)
                if (order_product.count() == 1):
                    for op in order_product:
                        op.quantity = op.quantity + int(request.POST.get('quantity'))
                        op.save()
                else:
                    order_product = Order_Products()
                    order_product.quantity = request.POST.get('quantity')
                    order_product.producttype = product
                    order_product.numberoforder = order
                    order_product.save()
            else:
                messages.error(request,'Debes de seleccionar un producto')
        list_order_product = Order_Products.objects.filter(numberoforder_id=order.id)
        context = {
            'products':product_suppliers,
            'supplier':supplier,
            'order_id':request.session['id_order'],
            'order_products':list_order_product
        }
    return render(request, "manager/orders/list_products.html", context)

def send_order_email(request):
    order = Order.objects.get(id=request.session['id_order'])
    order_products = Order_Products.objects.filter(numberoforder_id=order.id)
    if (order_products.count() <= 0):
        messages.error(request, 'Correo no enviado al proveedor: ' + order.supplier.name + ', debido a que no se adjuntaron productos al pedido.')
        order.delete()
        del request.session['id_order']
        return redirect('suppliers')
    context = {
        'supplier':order.supplier,
        'order_products':order_products,
        'numberoforder':order.id,
        'date':order.orderdate,
        'validation_key':order.validation_key
    }
    template = get_template('manager/orders/email_manual_order.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Pedido de Productos',
        'Realizacion de pedido, de la empresa Dashtory',
        settings.EMAIL_HOST_USER,
        [order.supplier.email]
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    order.state = "Enviado"
    order.save()
    messages.success(request, 'Correo enviado al proveedor: ' + order.supplier.name + ', con los productos solicitados.')
    del request.session['id_order']
    return redirect('suppliers')

def btn_cancel_an_order(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    del request.session['id_order']
    return redirect('suppliers')


def suppliers(request):
    suppliers = Supplier.objects.filter(active=True)
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
    supplier = Supplier.objects.get(id = id,active=True)
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

def validation_order(request, key, id):
    try:
        order = Order.objects.get(id=id)
    except:
        context = {'messages':"Numero de pedido, invalido."}
        return render(request,"manager/orders/messages_confirm.html",context) 
    if(request.method == 'GET'):
        if (order):
            if(order.validation_key == key):
                if(order.state == "En Proceso"):
                    context = {'messages':"Este enlace ya fue utilizado, y se confirmo la entrega."}
                else:
                    order.state = "En Proceso"
                    order.save()
                    context = {'messages':"Confirmacion de entrega de producto aceptada"}
            else:
                context = {'messages':"Llave de validacion incorrecta"}
        else: 
            context = {'messages':"Numero de pedido invalido"}
    return render(request,"manager/orders/messages_confirm.html",context) 

def list_orders(request):
    orders = Order.objects.all()
    context = {
            'orders':orders
        }
    return render(request, "manager/orders/list_orders.html", context)   

def details_of_order(request, id):
    try:
        order = Order.objects.get(id=id)
    except:
        messages.error(request,"Numero de pedido invalido")
        return redirect("list_orders")
    orders_products = Order_Products.objects.filter(numberoforder_id=id)
    if request.method == 'GET':
        context = {
            'id_order':id,
            'supplier':order.supplier.name,
            'order_products':orders_products,
            'state':order.state,
            'date':order.orderdate
        }
    else: 
        try:
            product = ProductType.objects.get(id = request.POST.get('id_product'))
            order_product = Order_Products.objects.get(numberoforder_id=id,producttype_id=product.id)
            order_product.date = datetime.now()
            order_product.save()
            if(int(request.POST.get('quantity')) > 0):
                newproduct=GroupProduct.objects.create(ingressdate=datetime.now(), expirationdate=request.POST.get('expirationdate'), quantity=order_product.quantity, supplier_id=order_product.numberoforder.supplier.id, producttype_id=order_product.producttype.id)
                newproduct.save()
                product.quantity=product.quantity+newproduct.quantity
                product.save()
                check_products = Order_Products.objects.filter(numberoforder_id=id).filter(date=None).count()
                if check_products == 0 and order.state == "En Proceso":
                    order.state = "Procesado"
                    order.save()
                messages.success(request, "Se ingreso la cantidad correctamente")
            else:
                messages.error(request, "Existio un error en la cantidad por favor intentelo de nuevo")
        except:
            messages.error(request, "El producto seleccionado no existe")
        context = {
                'id_order':id,
                'supplier':order.supplier.name,
                'order_products':orders_products,
                'state':order.state,
                'date':order.orderdate
            }
    return render(request, "manager/orders/detail_order.html",context)

