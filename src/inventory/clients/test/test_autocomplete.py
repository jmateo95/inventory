import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.clients.models import Client
from inventory.clients.views import get_nit_for_autocomplete, get_upc_for_autocomplete
from inventory.products.models import ProductType, Category, Supplier, GroupProduct

@pytest.mark.django_db
def test_autocomplete_nit():
    Client.objects.create (nit = '12345678', name = 'Juan', last_name = 'Lopez')
    Client.objects.create (nit = '87654321', name = 'Maria', last_name = 'Lopez')
    Client.objects.create (nit = '85236741', name = 'Carlos', last_name = 'Lopez')
    Client.objects.create (nit = '12358741', name = 'Estela', last_name = 'Lopez')
    Client.objects.create (nit = '45632187', name = 'Estefany', last_name = 'Lopez')
    assert get_nit_for_autocomplete('123').count()==2

@pytest.fixture
def category(db) -> Category:
    return Category.objects.create(name="categoria")   

@pytest.fixture
def productType(db, category) -> ProductType:
    return ProductType.objects.create(name="product",quantity=10,category=category) 

@pytest.fixture
def supplier(db) -> Supplier:
    return Supplier.objects.create(email="supplier@gmail.com",name="supplier",active=True,address="Quetzaltenango",phone=58479665)
    

@pytest.mark.django_db
def test_autocomplete_upc(db, productType, supplier):
    GroupProduct.objects.create(upc=1222,ingressdate='2021-10-21 13:49:55.179584-04',expirationdate='2023-10-21 13:49:55.179584-04',
    quantity=5,producttype= productType,supplier=supplier)
    GroupProduct.objects.create(upc=1223,ingressdate='2021-10-21 13:49:55.179584-04',expirationdate='2023-10-21 13:49:55.179584-04',
    quantity=5,producttype= productType,supplier=supplier)
    GroupProduct.objects.create(upc=2222,ingressdate='2021-10-21 13:49:55.179584-04',expirationdate='2023-10-21 13:49:55.179584-04',
    quantity=5,producttype= productType,supplier=supplier)
    GroupProduct.objects.create(upc=3333,ingressdate='2021-10-21 13:49:55.179584-04',expirationdate='2023-10-21 13:49:55.179584-04',
    quantity=5,producttype= productType,supplier=supplier)
    assert get_upc_for_autocomplete('12').count()==2
