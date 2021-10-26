from django.contrib.messages.api import error
from django.shortcuts import render
from datetime import datetime
from django.db.models import Sum
import json
from inventory.clients.models import ProductSale, Sale

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
    #print('.........')
    #print(str(ventas.query))
    return ('{"title": {"text": "Ventas del Mes"},"tooltip": {"trigger": "axis"},"legend": {"data": ["Ventas"]},"grid": {"left": "3%","right": "4%","bottom": "3%","containLabel": "true"},"toolbox": {"show": "true","feature": {"dataZoom": {"yAxisIndex": "none"},"dataView": { "readOnly": "false" },"magicType": { "type": ["line", "bar"] },"restore": {},"saveAsImage": {}}},"xAxis": {"type": "category","boundaryGap": "false","data": '+serialize(ventas, 'datetime__day')+'},"yAxis": {"type": "value"},"series": [{"name": "Ventas","type": "line","stack": "Total","data": '+serialize(ventas,'total')+'}]}')

def product_most_worst(firstdayofmonth):
    #pubs=ProductSale.objects.select_related('sale', 'product', 'product__producttype', 'product__producttype__category').values_list('sale_id', 'product_id','product__producttype_id', 'product__producttype__category_id', 'product__producttype__category__name', 'sale__datetime')
    #pubs=ProductSale.objects.select_related('sale', 'product', 'product__producttype', 'product__producttype__category').values_list('product__producttype_id', 'product__producttype__name', 'product__producttype__category_id', 'product__producttype__category__name', 'quantity', 'total', 'sale_id', 'product_id', 'sale__datetime')
    #pubs=ProductSale.objects.filter(sale__datetime__gte=firstdayofmonth).select_related('sale', 'product', 'product__producttype', 'product__producttype__category').values_list('product__producttype_id', 'product__producttype__name', 'product__producttype__category_id', 'product__producttype__category__name', 'quantity', 'total', 'sale__datetime')
    pubs=ProductSale.objects.filter(sale__datetime__gte=firstdayofmonth).select_related('sale', 'product', 'product__producttype', 'product__producttype__category').values_list('product__producttype_id', 'product__producttype__name', 'quantity', 'total').values('product__producttype_id', 'product__producttype__name').annotate(productos=Sum('quantity')).annotate(total=Sum('total')).order_by('productos')
    hola=None
    hola2=None
    if (len(pubs)>0):
        hola=pubs[len(pubs)-1]
        hola2=pubs[0]
    #print(hola)
    return {'most': hola, 'worst':hola2}


def category_most_worst(firstdayofmonth):
    pubs=ProductSale.objects.filter(sale__datetime__gte=firstdayofmonth).select_related('sale', 'product', 'product__producttype', 'product__producttype__category').values_list('product__producttype_id', 'product__producttype__name', 'quantity', 'total').values('product__producttype__category_id', 'product__producttype__category__name').annotate(productos=Sum('quantity')).annotate(total=Sum('total')).order_by('productos')
    hola=None
    hola2=None
    if (len(pubs)>0):
        hola=pubs[len(pubs)-1]
        hola2=pubs[0]
    return {'most': hola, 'worst':hola2}
    

def dashboard(request):
    option=[]
    name=[]
    firstdayofmonth=FirstDayOfMonth()
    #Grafico de ventas del mes
    name.append('id_0')
    option.append(sales_month(firstdayofmonth))

    product=product_most_worst(firstdayofmonth)
    category=category_most_worst(firstdayofmonth)

    json_option = json.dumps(option)
    json_name = json.dumps(name)
    context = {
        'options' :json_option ,
        'names':json_name,
        'most_product':product['most'],
        'worst_product':product['worst'],
        'most_category':category['most'],
        'worst_category':category['worst'],
        
    }
    return render(request,"dashboard/dashboard.html",context)
