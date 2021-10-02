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
from inventory.products.views import modify, modify_order_product, create_category
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', index, name='home'),
    path ('nombre/', index, name='path2'),
    path('dashboard/row/graph/add', addgraph,name='add_graph'), 
    # Paths para las funciones de manager 
    path('manager/form_edit_order/', modify, name='list'),
    path('manager/edit_order/<int:id>/', modify_order_product, name='edit_order'),
    path('manager/create_category/', create_category, name='create_category')
]
