"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path, include
from inventory.index.views import index, addgraph

from inventory.products.views import *
from inventory.users.views import adduser, newuser, listuser, deleteuser, edituser
from inventory.clients.views import list_client, modal_register_client, register_sale, autocomplete_client, autocomplete_upc, insert_product,search_client, delete_temp_product, transacction, transacction_cashier

from inventory.products.views import modify_order_product, create_product_type, list_categories, listproduct, listlot, list_products_supplier, send_order_email, manual_purchase, btn_cancel_an_order, validation_order, list_orders, details_of_order
from inventory.dashboard.views import dashboard
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', index, name='home'),
    path ('nombre/', index, name='path2'),
    path('dashboard/row/graph/add', addgraph,name='add_graph'), 
    #Jonathan
    path('administrator/adduser/', adduser, name='adduser'),
    path('administrator/newuser/', newuser, name='newuser'),
    path('administrator/listuser/', listuser, name='listuser'),
    path('administrator/deleteuser/<int:id>/', deleteuser, name='deleteuser'),
    path('administrator/edituser/<int:id>/', edituser, name='edituser'),
    path('administrator/dashboard/', dashboard, name='dashboard'),


    path('manager/listproduct/', listproduct, name='listproduct'),
    path('manager/manual_purchase/<int:id>/', manual_purchase, name='manual_purchase'),

    path('manager/listlot/<int:id>/', listlot, name='list_lot'),


    
    # Paths para las funciones de manager 
    path('manager/edit_product/<int:id>/', modify_order_product, name='edit_product'),
    path('manager/create_category/', create_category, name='create_category'),
    path('manager/create_supplier/', create_supplier, name='create_supplier'),
    path('manager/create_product_type/', create_product_type, name='type_create'),
    path('manager/list_categories/', list_categories, name='list_categories'),
    path('manager/product_suppliers/<int:id>/', product_suppliers, name='product_suppliers'),
    path('manager/manual_order/<int:id>/<int:nuevo>/', list_products_supplier, name='manual_order'),
    path('manager/remove_product/<int:id_supplier>/<int:id_product_order>/', delete_product_an_order, name='remove_product'),
    path('manager/send_order_email/', send_order_email, name='send_order_email'),
    path('manager/supplier_products/<int:id>/', supplier_products, name='supplier_products'),
    path('manager/suppliers/', suppliers, name='suppliers'),
    path('manager/deletesupplier/<int:id>/', deletesupplier, name='deletesupplier'),
    path('manager/deleteproductsupplier/<int:id>/<int:id2>/', deleteproductsupplier, name='deleteproductsupplier'),
    path('manager/btn_cancel_an_order/<int:id>', btn_cancel_an_order, name='btn_cancel_an_order'),
    path('manager/list_orders/', list_orders, name='list_orders'),
    path('manager/list_detail/<int:id>', details_of_order, name='list_detail'),
    path('manager/cancel_order/<int:id>/', cancel_order, name="cancel_order"),
    # Paths para el cajero
    path('confirm_order/<str:key>/<int:id>', validation_order, name='validation_order'),
    path('cashier/register_client/', modal_register_client, name='register_client'),
    path('cashier/register_sale/', register_sale, name='register_sale'),
    path('api/autocomplete_client/', autocomplete_client, name='autocomplete_client'),
    path('api/autocomplete_upc/', autocomplete_upc, name='autocomplete_upc'),
    path('api/insert_product/', insert_product, name='insert_product'),
    path('client/search_client/', search_client, name='search_client'),
    path('client/delete_temp_product/', delete_temp_product, name='delete_temp_product'),
    path('cashier/list_client', list_client, name='list-client'),
    path('cashier/transactions/', transacction_cashier, name='transactions-cashier'),
    path('administrator/transactions_manager/', transacction, name='transactions')
    
]

