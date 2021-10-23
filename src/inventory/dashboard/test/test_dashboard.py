import pytest
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()

from inventory.dashboard.views import FirstDayOfMonth, sales_month, serialize
from inventory.clients.models import Sale
from django.db.models import Sum

def test_FirstDayOfMonth():
    dia=""+str(FirstDayOfMonth())
    dia=dia[8:10]
    assert dia=='01'


def test_serialize():
    lista=[{'camisa':'uno'},{'camisa':'dos'},{'camisa':'tres'}]
    variable=serialize(lista, 'camisa')
    assert variable == '[uno,dos,tres]'

@pytest.mark.django_db
def test_sales_month():
    firstdayofmonth=FirstDayOfMonth()
    variable=sales_month(firstdayofmonth)
    ventas=Sale.objects.extra(select={'dia':'EXTRACT(DAY FROM datetime)', 'total':'total'}).filter(datetime__gte=firstdayofmonth).values('datetime__day').annotate(total=Sum('total')).order_by('datetime__day')
    variable2=('{"title": {"text": "Ventas del Mes"},"tooltip": {"trigger": "axis"},"legend": {"data": ["Ventas"]},"grid": {"left": "3%","right": "4%","bottom": "3%","containLabel": "true"},"toolbox": {"show": "true","feature": {"dataZoom": {"yAxisIndex": "none"},"dataView": { "readOnly": "false" },"magicType": { "type": ["line", "bar"] },"restore": {},"saveAsImage": {}}},"xAxis": {"type": "category","boundaryGap": "false","data": '+serialize(ventas, 'datetime__day')+'},"yAxis": {"type": "value"},"series": [{"name": "Ventas","type": "line","stack": "Total","data": '+serialize(ventas,'total')+'}]}')
    assert variable==variable2