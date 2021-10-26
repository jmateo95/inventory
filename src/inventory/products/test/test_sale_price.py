import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.products.models import ProductType, Category, Supplier, SalePrice

@pytest.fixture
def category(db) -> Category:
    return Category.objects.create(name="categoria")    

@pytest.fixture
def productType(db, category) -> ProductType:
    return ProductType.objects.create(name="product",quantity=10,category=category)        
@pytest.fixture
def salePrice(db, productType) -> SalePrice:
    return SalePrice.objects.create(channgeddate='2021-10-21 13:49:55.179584-04',price=20.50,producttype=productType) 

def test_saleprice_quantity(db, salePrice):    
    assert salePrice.producttype.name=="product"

