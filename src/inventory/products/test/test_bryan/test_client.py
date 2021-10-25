import pytest
import os,django

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.clients.views import check_exist_nit
from inventory.clients.models import Client

@pytest.mark.django_db
def test_check_existence_nit():
    Client.objects.create (nit = '12345678', name = 'Juan')
    Client.objects.create (nit = '87654321', name = 'Maria')
    Client.objects.create (nit = '85236741', name = 'Carlos')
    Client.objects.create (nit = '63258741', name = 'Estela')
    Client.objects.create (nit = '45632187', name = 'Estefany')
    assert not check_exist_nit(Client.objects.all(), '12345679') 