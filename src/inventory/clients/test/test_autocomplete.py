import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.clients.models import Client
from inventory.clients.views import get_nit_for_autocomplete

