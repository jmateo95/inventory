import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.products.models import Supplier
from ddf import G, N, F

@pytest.fixture
def common_create_supplier():
    return Supplier.objects.create (
        email = 'prueba@gmail.com',
        name = 'Distribuidor Prueba'
    )

@pytest.mark.django_db
def test_create_supplier(common_create_supplier):
    supplier = common_create_supplier
    assert supplier.active