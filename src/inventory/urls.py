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

from inventory.products.views import modify_order_product, create_category, create_supplier
from inventory.users.views import adduser, newuser, listuser, deleteuser

from inventory.products.views import modify_order_product, create_product_type, list_categories, listproduct
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

    path('manager/listproduct/', listproduct, name='listproduct'),
    
    
    # Paths para las funciones de manager 
    path('manager/edit_product/<int:id>/', modify_order_product, name='edit_product'),
    path('manager/create_category/', create_category, name='create_category'),
    path('manager/create_supplier/', create_supplier, name='create_supplier'),
    path('manager/create_product_type/', create_product_type, name='type_create'),
    path('manager/list_categories/', list_categories, name='list_categories'),
]
