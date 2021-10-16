from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now

class Category (models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)

    def __str__(self):
        return "%s" % (self.name)
    
class Supplier(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.CharField(max_length=200, unique=True)
    name=models.CharField(max_length=200)
    active =models.BooleanField(default=True)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)

    def __str__(self):
        return "%s" % (self.name)



class ProductType (models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200, unique=True)
    orderpoint=models.IntegerField(null=True)
    orderquantity=models.IntegerField(null=True)
    quantity=models.IntegerField(default=0)
    category=models.ForeignKey(Category, on_delete=CASCADE, related_name='Category_Products')

    def __str__(self):
        return "%s" % (self.name)
    
    def get_edit_url(self):
        return 'edit_product/'+str(self.id)+"/"


class SalePrice(models.Model):
    id=models.AutoField(primary_key=True)
    channgeddate=models.DateTimeField()
    price=models.DecimalField(max_digits=8, decimal_places=2)
    producttype=models.ForeignKey(ProductType, on_delete=CASCADE, related_name='ProductType_SalesPrice')


class ProductSupplier(models.Model):
    id=models.AutoField(primary_key=True)
    supplier=models.ForeignKey(Supplier, on_delete=CASCADE, related_name='Supplier_Producttype')
    producttype=models.ForeignKey(ProductType, on_delete=CASCADE, related_name='Producttype_Supplier')

class GroupProduct(models.Model):
    upc=models.AutoField(primary_key=True)
    ingressdate=models.DateTimeField(default=now)
    expirationdate=models.DateTimeField()
    quantity=models.IntegerField()
    supplier=models.ForeignKey(Supplier, on_delete=CASCADE, related_name='Supplier_GropuProducts')

class Order(models.Model):
    id=models.AutoField(primary_key=True)
    orderdate=models.DateTimeField(default=now)
    state=models.CharField(max_length=200, default='No Enviado')
    supplier=models.ForeignKey(Supplier, on_delete=CASCADE, related_name='Order_Supplier')

class Order_Products(models.Model):
    id=models.AutoField(primary_key=True)
    quantity=models.IntegerField()
    producttype=models.ForeignKey(ProductType, on_delete=CASCADE, related_name='Order_Producttype')
    numberoforder=models.ForeignKey(Order, on_delete=CASCADE, related_name='Number_Order')