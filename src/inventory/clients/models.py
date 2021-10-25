from django.db import models
from ..users.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from ..products.models import GroupProduct
# Create your models here.

class Client(models.Model):
    id=models.AutoField(primary_key=True)
    nit=models.CharField(unique=True, max_length=20, null=True)
    name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200, null=True)
    address=models.CharField(max_length=200, null=True)
    phone=models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name+" "+self.last_name

class Sale(models.Model):
    id=models.AutoField(primary_key=True)
    client=models.ForeignKey(Client,on_delete=SET_NULL,null=True, related_name='Sale_Client')
    cashier=models.ForeignKey(User,on_delete=CASCADE, related_name='Sale_Cashier')
    datetime=models.DateTimeField()
    total=models.DecimalField(max_digits=8, decimal_places=2)

class ProductSale(models.Model):
    id=models.AutoField(primary_key=True)
    product=models.ForeignKey(GroupProduct,on_delete=CASCADE, related_name='Sale_Cashier')
    sale=models.ForeignKey(Sale,on_delete=CASCADE, related_name='ProductSale_Sale')
    quantity=models.IntegerField(default = 1)
    total=models.DecimalField(max_digits=8, decimal_places=2)

class TempProductSale(models.Model):
    id=models.AutoField(primary_key=True)
    number=models.IntegerField()
    product=models.ForeignKey(GroupProduct,on_delete=CASCADE, related_name='Temp_Sale_Cashier')
    quantity=models.IntegerField(default = 1)
    total=models.DecimalField(max_digits=8, decimal_places=2)