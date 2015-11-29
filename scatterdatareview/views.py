from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import math
import json

# Create your views here.
def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('scatterdatareview/login.html', c)

def auth_user(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/scatter/review', {'username': username})
    else:
        return HttpResponseRedirect('/scatter/login', {'username': 'Anony'})

def logout(request):
    auth.logout(request)
    return render_to_response('scatterdatareview/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = User.objects.create_user(username, email, password)
        if user is not None:
            return HttpResponseRedirect('/scatter/login')
        
    c = {}
    c.update(csrf(request))
    return render_to_response('scatterdatareview/register.html', c)

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/scatter/login')
    
    return render_to_response('scatterdatareview/review.html', {'username': request.user.username})

def getDataset(request):
    f = open('E:/GeoVis/scatterdatareview/1.txt', 'r')
    dataNum = int(f.readline())
    jsData = []
    for i in range(dataNum):
        point = []
        x = float(f.readline())
        y = float(f.readline())
        v = float(f.readline())
        point.append(x)
        point.append(y)
        point.append(v)
        jsData.append(point)
    try:
        json_data = json.dumps(jsData)
    except Exception as ex:
        print ex
    f.close()    
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def saveClusterData(request):
    if request.method == 'POST':
        dataIndex = request.POST['dataIndex']
        f = open('E:/GeoVis/scatterdatareview/2.txt', 'w')
        f.writeline(dataIndex);
        f.close()