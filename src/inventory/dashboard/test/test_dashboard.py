import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.dashboard.views import FirstDayOfMonth

def test_FirstDayOfMonth():
    dia=""+str(FirstDayOfMonth())
    dia=dia[8:10]
    assert dia=='01'
