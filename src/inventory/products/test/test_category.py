import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.products.views import prueba_suma
from inventory.products.models import Category
from ddf import G, N, F

@pytest.fixture
def category_creation():
    return N(Category(name='Prueba 1'))

def test_create_category(category_creation):
    print (category_creation.name)

def test_prueba_suma():
    assert 3 == prueba_suma(3,0)