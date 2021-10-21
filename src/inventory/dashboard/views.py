from django.contrib.messages.api import error
from django.shortcuts import render
from datetime import datetime
from django.db.models import Sum
import json
from inventory.clients.models import Sale

# Create your views here.
def FirstDayOfMonth():
    return datetime.today().replace(day=1).replace(hour=00).replace(minute=00).replace(second=00)

def serialize(objects, name):
    array="["
    for object in objects:
        array+=str(object[name])+","
    array=(array[:-1])
    array+="]"
    return array

def sales_month(firstdayofmonth):
    ventas=Sale.objects.extra(select={'dia':'EXTRACT(DAY FROM datetime)', 'total':'total'}).filter(datetime__gte=firstdayofmonth).values('datetime__day').annotate(total=Sum('total')).order_by('datetime__day')
    return ('{"title": {"text": "Ventas del Mes"},"tooltip": {"trigger": "axis"},"legend": {"data": ["Ventas"]},"grid": {"left": "3%","right": "4%","bottom": "3%","containLabel": "true"},"toolbox": {"show": "true","feature": {"dataZoom": {"yAxisIndex": "none"},"dataView": { "readOnly": "false" },"magicType": { "type": ["line", "bar"] },"restore": {},"saveAsImage": {}}},"xAxis": {"type": "category","boundaryGap": "false","data": '+serialize(ventas, 'datetime__day')+'},"yAxis": {"type": "value"},"series": [{"name": "Ventas","type": "line","stack": "Total","data": '+serialize(ventas,'total')+'}]}')


def dashboard(request):
    option=[]
    name=[]
    firstdayofmonth=FirstDayOfMonth()
    
    #Grafico de ventas del mes
    name.append('id_0')
    option.append(sales_month(firstdayofmonth))

    json_option = json.dumps(option)
    json_name = json.dumps(name)
    context = {
        'options' :json_option ,
        'names':json_name,
    }
    return render(request,"dashboard/dashboard.html",context)
