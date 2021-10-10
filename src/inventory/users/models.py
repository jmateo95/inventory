from django.db import models
from django.contrib.auth.models import AbstractUser


class Rol(models.Model):

    id=models.AutoField(primary_key=True)
    rol=models.CharField('Rol', max_length=50, unique=True)

    class Meta:
        verbose_name= 'Rol'
        verbose_name_plural= 'Roles'

    def __str__(self):
        return self.rol
    def get_rol(self):
        return self.rol

class User (AbstractUser):
    rol=models.ForeignKey(Rol, on_delete=models.CASCADE, blank=True, null=True, default=1)

    def get_delete_url(self):
        return 'deleteuser/'+str(self.id)+"/"

    def get_edit_url(self):
        return 'edituser/'+str(self.id)+"/"
