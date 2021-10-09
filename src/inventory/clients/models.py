from django.db import models

# Create your models here.

class Client(models.Model):
    id=models.AutoField(primary_key=True)
    nit=models.CharField(unique=True, max_length=20, null=True)
    name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200, null=True)
    address=models.CharField(max_length=200, null=True)
    phone=models.CharField(max_length=20, null=True)

    def __str__(self):
        return "%s" % (self.name)