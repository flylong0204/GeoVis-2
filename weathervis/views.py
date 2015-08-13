from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from netCDF4 import Dataset
from django.http.response import JsonResponse
import numpy, json
from overlayprocessing import *
import cv2
import math

def obj_dict(obj):
    return obj.__dict__

# Create your views here.
def index(request):
    return render_to_response('weathervis/weathervis.html')

def glyphValues(request):
    #level = Math.round(request.GET['level'])
    #model = request.GET['model']
    #variable = request.GET['var']
    #date = request.GET['date']
    level = 3
    infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
    rootgrp = Dataset(infoPath, format='NETCDF4')
    xfLen = len(rootgrp.dimensions['xf'])
    yfLen = len(rootgrp.dimensions['yf'])
    ensLen = len(rootgrp.dimensions['ens'])
    lons_fcst = numpy.ma.getdata(rootgrp.variables['lons_fcst'][:][:])
    lats_fcst = numpy.ma.getdata(rootgrp.variables['lats_fcst'][:][:])
    rootgrp.close()
    f = open('E:/Data/00_24/apcp_ens/2002010200.apcp', 'rb')
    dataValues = numpy.fromfile(f, dtype=numpy.float32).reshape((ensLen, yfLen, xfLen))
    f.close()
    jsData = []
    xNum = int(round(xfLen / level))
    yNum = int(round(yfLen / level))
    meanArray = numpy.zeros(ensLen)
    for i in range(0, yNum):
        for j in range(0, xNum):
            varMean = 0
            for k in range(0, ensLen):
                meanArray[k] = 0
                for bi in range(0, level):
                    for bj in range(0, level):
                        meanArray[k] += dataValues[k][i * level + bi][j * level + bj]
                meanArray[k] /= (level * level)
                varMean += meanArray[k]
            varMean /= ensLen
            varVari = 0
            for k in range(0, ensLen):
                varVari += pow(meanArray[k] - varMean, 2)
            varVari /= ensLen
            glyphData = {}
            glyphData['mean'] = varMean
            glyphData['var'] = varVari
            glyphData['lon'] = float(lons_fcst[i * level][j * level])
            glyphData['lat'] = float(lats_fcst[i * level][j * level])
            jsData.append(glyphData)
    try:
        json_data = json.dumps(jsData)
    except Exception as ex:
        print ex    
    return JsonResponse(json_data, safe=False)

def kmeansValues(request):
    level = int(request.GET['level'])
    infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
    rootgrp = Dataset(infoPath, format='NETCDF4')
    lons_fcst = numpy.ma.getdata(rootgrp.variables['lons_fcst'][:][:])
    lats_fcst = numpy.ma.getdata(rootgrp.variables['lats_fcst'][:][:])
    rootgrp.close()
    
    img = cv2.imread('E:/Geovis/weathervis/test.png')
    nodeCluster = NodeCluster()
    nodeCluster.processImage(img, level * 50)
    jsData = []
    for index in nodeCluster.labelIndex:
        x = round(index['X'])
        y = round(index['Y'])
        pixelNum = index['pixelNum']
        glyphData = {}
        glyphData['r'] = math.sqrt(pixelNum) * (lons_fcst[1][1] - lons_fcst[1][0]) / 3
        glyphData['lon'] = float(lons_fcst[y][x])
        glyphData['lat'] = float(lats_fcst[y][x])
        jsData.append(glyphData)
    try:
        json_data = json.dumps(jsData)
    except Exception as ex:
        print ex    
    return JsonResponse(json_data, safe=False)

def hierarValues(request):
    level = int(request.GET['level'])
    infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
    rootgrp = Dataset(infoPath, format='NETCDF4')
    lons_fcst = numpy.ma.getdata(rootgrp.variables['lons_fcst'][:][:])
    lats_fcst = numpy.ma.getdata(rootgrp.variables['lats_fcst'][:][:])
    rootgrp.close()
    
    img = cv2.imread('E:/Geovis/weathervis/test.png')
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    test = img[0, 0]
    nodeCluster = NodeCluster()
    nodeCluster.processImageHier(img, level * 50)
    proc = OverlayProcessor(nodeCluster)
    proc.heuristicSolve()
    jsData = []
    for index in nodeCluster.labelIndex:
        x = round(index['x'])
        y = round(index['y'])
        pixelNum = index['nodeNum']
        glyphData = {}
        glyphData['r'] = math.sqrt(pixelNum) * (lons_fcst[1][1] - lons_fcst[1][0]) / 3
        glyphData['lon'] = float(lons_fcst[y][x])
        glyphData['lat'] = float(lats_fcst[y][x])
        jsData.append(glyphData)
    try:
        json_data = json.dumps(jsData)
    except Exception as ex:
        print ex    
    return JsonResponse(json_data, safe=False)
            