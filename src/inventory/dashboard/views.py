from django.shortcuts import render

# Create your views here.

def dashboard(request):
    option=[]
    name=[]
    option.append('{"title": {"text": "ejempo_0"},"xAxis": {"type": "category","data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},"yAxis": {"type": "value"},"series": [{"data": [150, 230, 224, 218, 135, 147, 260],"type": "line","name": "uno"},{"data": [160, 220, 214, 228, 145, 157, 270],"type": "line","name": "dos"}]}')
    option.append('{"title": {"text": "ejempo_1"},"xAxis": {"type": "category","data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},"yAxis": {"type": "value"},"series": [{"data": [150, 230, 224, 218, 135, 147, 260],"type": "line","name": "uno"},{"data": [160, 220, 214, 228, 145, 157, 270],"type": "line","name": "dos"}]}')
    option.append('{"title": {"text": "ejempo_2"},"xAxis": {"type": "category","data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},"yAxis": {"type": "value"},"series": [{"data": [150, 230, 224, 218, 135, 147, 260],"type": "line","name": "uno"},{"data": [160, 220, 214, 228, 145, 157, 270],"type": "line","name": "dos"}]}')
    name.append('id_0')
    name.append('id_1')
    name.append('id_2')

    context = {
    }
    return render(request,"dashboard/dashboard.html",context)
