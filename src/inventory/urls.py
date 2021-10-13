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
from django.contrib import admin
from django.urls import path, include
from inventory.index.views import index, addgraph

from inventory.products.views import modify_order_product, create_category, create_supplier, product_suppliers
from inventory.users.views import adduser, newuser, listuser, deleteuser, edituser
from inventory.clients.views import modal_register_client
from inventory.products.views import modify_order_product, create_product_type, list_categories, listproduct, list_suppliers, list_products_supplier, send_order_email
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

    path('manager/listproduct/', listproduct, name='listproduct'),
    
    
    # Paths para las funciones de manager 
    path('manager/edit_product/<int:id>/', modify_order_product, name='edit_product'),
    path('manager/create_category/', create_category, name='create_category'),
    path('manager/create_supplier/', create_supplier, name='create_supplier'),
    path('manager/create_product_type/', create_product_type, name='type_create'),
    path('manager/list_categories/', list_categories, name='list_categories'),
    path('manager/product_suppliers/<int:id>/', product_suppliers, name='product_suppliers'),
    path('manager/list_supplier/', list_suppliers, name='list_suppliers'),
    path('manager/manual_order/<int:id>/', list_products_supplier, name='manual_order'),
    path('manager/send_order_email/', send_order_email, name='send_order_email'),
    # Paths para el cajero
    path('cashier/register_client/', modal_register_client, name='register_client'),
]
