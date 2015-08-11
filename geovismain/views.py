from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geovismain.models import Dataset, User
from geovismain.serializer import UserSerializer
from netCDF4 import Dataset

import json, base64
from django.http.response import JsonResponse

@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def data_value(request):
    if request.method == 'GET':
        # read the metadata
        rootgrp = Dataset('E:/Data/00_24/info.nc', format='NETCDF4')
        xfLen = len(rootgrp.dimensions['xf'])
        yfLen = len(rootgrp.dimensions['yf'])
        rootgrp.close()
        
        # read the data
        file = open('E:/Data/00_24/mslp_mean/2002010200.mslp', 'rb')
        temp = file.read()
        file.close()
        b64_text = base64.b64encode(temp)
        
        
        jsData = {}
        jsData['data'] = b64_text
        jsData['name'] = 'mslp mean'
        jsData['xlen'] = xfLen
        jsData['ylen'] = yfLen
        jsData['xstep'] = 1
        jsData['ystep'] = 1
        jsData['xbegin'] = 0
        jsData['ybegin'] = 0 
        json_data = json.dumps(jsData)
        return JsonResponse(json_data, safe=False)
        
        