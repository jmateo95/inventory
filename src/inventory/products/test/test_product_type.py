import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.products.models import ProductType, Category

@pytest.fixture
def category(db) -> Category:
    return Category.objects.create(name="categoria")   

@pytest.mark.django_db
def test_product_type_creation(db, category):
    prod=ProductType.objects.create(name="product",quantity=10,category=category)
    assert str(prod)== 'product'
    