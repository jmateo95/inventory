import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.clients.models import Client

@pytest.fixture
def client(db) -> Client:
    return Client.objects.create(nit="12315646",name="Juan",last_name="Perez",address="Quetzaltenango",phone="12345678") 

def test_concat_client_name(db, client):    
    assert str(client)=="Juan Perez"