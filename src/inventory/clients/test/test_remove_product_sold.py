import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.products.models import ProductType, Category, Supplier, GroupProduct
from inventory.clients.views import remove_products_from_stock

@pytest.fixture
def category(db) -> Category:
    return Category.objects.create(name="categoria")    

@pytest.fixture
def productType(db, category) -> ProductType:
    return ProductType.objects.create(name="product",quantity=10,category=category)        

@pytest.fixture
def supplier(db) -> Supplier:
    return Supplier.objects.create(email="supplier@gmail.com",name="supplier",active=True,address="Quetzaltenango",phone=58479665)
    
@pytest.fixture
def groupProduct(db, productType, supplier) -> GroupProduct:
    return  GroupProduct(ingressdate='2021-10-21 13:49:55.179584-04',expirationdate='2023-10-21 13:49:55.179584-04',
    quantity=5,producttype= productType,supplier=supplier)


@pytest.mark.django_db
def test_check_existence_nit(db,groupProduct):
    remove_products_from_stock(5,groupProduct)
    assert  groupProduct.quantity==0 and groupProduct.producttype.quantity==5
