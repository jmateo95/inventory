import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.products.views import check_existence
from inventory.products.models import Category
from ddf import G, N, F

@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(
        name = 'Panaderia'
    )
    assert category.name == "Panaderia"
   
@pytest.mark.django_db
def test_check_existence_category():
    Category.objects.create(name='Higiene y belleza')
    Category.objects.create(name='Escolares')
    Category.objects.create(name='Carnes y Embutidos')
    Category.objects.create(name='Productos de limpieza')
    Category.objects.create(name='Pescaderia')
    assert not check_existence(Category.objects.all(), 'Juguetes', 1) 