from django.shortcuts import render
from django.shortcuts import render_to_response
import json
from django.http.response import JsonResponse

# Create your views here.
def index(request):
    return render_to_response('scatterdatareview/review.html')

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
    return JsonResponse(json_data, safe=False)