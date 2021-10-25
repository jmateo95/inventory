import pytest
import os,django

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.products.views import add_quantity_to_order_product, create_order_with__key, enter_the_order_product, validation_uuid
from inventory.products.models import Order, Order_Products, ProductType, Supplier, Category
from ddf import G, N, F

@pytest.fixture
def common_create_supplier():
    return Supplier.objects.create (
        email = 'prueba@gmail.com',
        name = 'Distribuidor Prueba'
    )

@pytest.fixture
def common_create_category():
    return Category.objects.create (
        name = 'Higiene'
    )

@pytest.fixture
def common_create_order():
    return G(Order)

@pytest.fixture
@pytest.mark.django_db
def common_create_product(common_create_category):
    return ProductType.objects.create(
        name = 'Producto 1',
        category = common_create_category
    )

@pytest.mark.django_db
def test_create_order(common_create_order):
    assert common_create_order.id == 1

@pytest.mark.django_db
def test_create_order_validation_key(common_create_supplier):
    assert create_order_with__key(common_create_supplier)

@pytest.mark.django_db
def test_validation_key_of_order(common_create_supplier):
    order = create_order_with__key(common_create_supplier)
    assert validation_uuid(str(order.validation_key))

@pytest.mark.django_db
def test_create_order_product(common_create_product, common_create_order):
    order_product = Order_Products.objects.create(
        quantity = 10,
        producttype = common_create_product, 
        numberoforder = common_create_order
    )
    assert order_product.id == 1

@pytest.mark.django_db
def test__update_quantity_to_order_product(common_create_order, common_create_product):
    Order_Products.objects.create(
        quantity = 10,
        producttype = common_create_product, 
        numberoforder = common_create_order
    )
    assert add_quantity_to_order_product(common_create_order, common_create_product, 15)

@pytest.mark.django_db
def test_add_quantity_to_order_product(common_create_order, common_create_product):
    order_product = Order_Products.objects.create(
        quantity = 10,
        producttype = common_create_product, 
        numberoforder = common_create_order
    )
    add_quantity_to_order_product(common_create_order, common_create_product, 15)
    order_product = Order_Products.objects.get(id=order_product.id)
    assert order_product.quantity == 25

@pytest.mark.django_db
def test_enter_the_order_product(common_create_product, common_create_supplier):
    order = create_order_with__key(common_create_supplier)
    order_product = Order_Products.objects.create(
        quantity = 10,
        producttype = common_create_product, 
        numberoforder = order
    )
    assert enter_the_order_product('2021-10-20', 15, order.supplier.id, order_product.producttype.id, common_create_product)

@pytest.mark.django_db
def test_verify_product_entry(common_create_product, common_create_supplier):
    order = create_order_with__key(common_create_supplier)
    order_product = Order_Products.objects.create(
        quantity = 10,
        producttype = common_create_product, 
        numberoforder = order
    )
    enter_the_order_product('2021-10-20', order_product.quantity, order.supplier.id, order_product.producttype.id, common_create_product)
    assert common_create_product.quantity == 10