import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.dashboard.views import FirstDayOfMonth, serialize

def test_FirstDayOfMonth():
    dia=""+str(FirstDayOfMonth())
    dia=dia[8:10]
    assert dia=='01'


def test_serialize():
    lista=[{'camisa':'uno'},{'camisa':'dos'},{'camisa':'tres'}]
    variable=serialize(lista, 'camisa')
    assert variable == '[uno,dos,tres]'
