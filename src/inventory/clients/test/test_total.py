import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.clients.models import TempProductSale
from inventory.products.models import ProductType, Category, Supplier, SalePrice
from inventory.clients.views import get_temp_total, get_total

@pytest.fixture
def category(db) -> Category:
    return Category.objects.create(name="categoria")    

@pytest.fixture
def productType(db, category) -> ProductType:
    return ProductType.objects.create(name="product",quantity=10,category=category)        
@pytest.fixture
def salePrice(db, productType) -> SalePrice:
    return SalePrice.objects.create(channgeddate='2021-10-21 13:49:55.179584-04',price=20.5,producttype=productType) 



def test_saleprice_quantity(db, salePrice):    
    assert get_total(10,salePrice)==205

@pytest.mark.django_db
def test_empty_temp():    
    assert get_temp_total()==0
