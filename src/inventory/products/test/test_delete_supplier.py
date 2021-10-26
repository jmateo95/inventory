import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()


from inventory.products.models import Supplier
from inventory.products.views import deactivate_supplier

@pytest.fixture
def supplier(db) -> Supplier:
    return Supplier(email="supplier@gmail.com",name="supplier",active=True,address="Quetzaltenango",phone=58479665)
    
@pytest.mark.django_db
def test_delete_supplier(db, supplier):
    deactivate_supplier(supplier)
    number=Supplier.objects.filter(name="supplier").count()
    assert number==1

@pytest.mark.django_db
def test_deactivate_supplier(db, supplier):
    deactivate_supplier(supplier)
    sup =Supplier.objects.get(name="supplier")
    assert sup.active==False