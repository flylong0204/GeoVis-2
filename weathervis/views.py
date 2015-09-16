from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from netCDF4 import Dataset
from django.http.response import JsonResponse
import numpy as np 
import json
from overlayprocessor import OverlayProcessor
from candidateselector import CandidateSelector
from uncertaintyprocessor import UncertaintyProcessor
from consistencyprocessor import ConsistencyProcessor
from skimage import measure
import cv2
import math

# Create your views here.
def index(request):
    return render_to_response('weathervis/weathervis.html')

def getApcpForecast(request):
    cached = 1
    jsData = []
    if cached == 0:
        infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
        rootgrp = Dataset(infoPath, format='NETCDF4')
        height = len(rootgrp.dimensions['yf'])
        width = len(rootgrp.dimensions['xf'])
        lons_fcst = np.ma.getdata(rootgrp.variables['lons_fcst'][:][:])
        lats_fcst = np.ma.getdata(rootgrp.variables['lats_fcst'][:][:])
        ens = len(rootgrp.dimensions['ens'])
        apcp = np.ma.getdata(rootgrp.variables['apcp_fcst_ens'][100][:][:][:])
        rootgrp.close()
        
        isoValues = [5, 10, 25]
        for index in isoValues:
            averageApcp = np.zeros((height, width), np.float32)
            for h in range(height):
                for w in range(width):
                    temp = 0
                    for e in range(ens):
                        temp += apcp[e][h][w]
                    averageApcp[h][w] = float(temp / ens)
            contours = measure.find_contours(averageApcp, index)
            data = []
            for n, contour in enumerate(contours):
                contourLen = len(contour[:, 1])
                coutourData = []
                for i in range(contourLen):
                    point = contour[i, :]
                    x = int(point[1]);
                    next_x = x + 1;
                    if (next_x >= width): next_x = width - 1;
                    y = int(point[0]);
                    next_y = y + 1;
                    if (next_y >= height): next_y = height - 1;
                    tempArray = []
                    if (x == next_x):
                        tempArray.append(float(lons_fcst[y][x]))
                    else:
                        tempArray.append(float((point[1] - x) * lons_fcst[y][next_x] + (next_x - point[1]) * lons_fcst[y][x]))
                    if (y == next_y):
                        tempArray.append(float(lats_fcst[y][x]))
                    else:
                        tempArray.append(float((point[0] - y) * lats_fcst[next_y][x] + (next_y - point[0]) * lats_fcst[y][x]))
                    coutourData.append(tempArray);
                data.append(coutourData)
            jsData.append(data)
        # save the data
        f = open('E:/GeoVis/weathervis/fcst.txt', 'w')
        f.write(str(len(jsData)) + "\n")
        for data in jsData:
            f.write(str(len(data)) + "\n")
            for line in data:
                f.write(str(len(line)) +"\n")
                for p in line:
                    f.write(str(p[0]) + "\n")
                    f.write(str(p[1]) + "\n")
        f.close()
    else:
        # load the data
        f = open('E:/GeoVis/weathervis/fcst.txt', 'r')
        dataNum = int(f.readline())
        for i in range(dataNum):
            data = []
            lineNum = int(f.readline())
            for j in range(lineNum):
                line = []
                pNum = int(f.readline())
                for k in range(pNum):
                    p = []
                    p.append(float(f.readline()))
                    p.append(float(f.readline()))
                    line.append(p)
                data.append(line)
            jsData.append(data)
        
    try:
        json_data = json.dumps(jsData)
    except Exception as ex:
        print ex    
    return JsonResponse(json_data, safe=False)

def generateCand(request):
    candNumber = int(request.GET['n'])
    infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
    rootgrp = Dataset(infoPath, format='NETCDF4')
    height = len(rootgrp.dimensions['yf'])
    width = len(rootgrp.dimensions['xf'])
    ens = len(rootgrp.dimensions['ens'])
    variableData = []
    apcp = np.ma.getdata(rootgrp.variables['apcp_fcst_ens'][100][:][:][:])
    variableData.append(apcp)
    rootgrp.close()
    
    averageData = np.zeros((height, width), np.float32)
    for e in range(ens):
        for h in range(height):
            for w in range(width):
                averageData[h][w] += apcp[e][h][w]
        for h in range(height):
            for w in range(width):
                averageData[h][w] /= ens
    
    #img = cv2.imread('E:/Geovis/weathervis/test.png')
    #img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = np.zeros((height, width), np.uint8)
    max_value = np.amax(averageData)
    for h in range(height):
        for w in range(width):
            img[h][w] = np.uint8(averageData[h][w] / max_value * 255)
    candSelector = CandidateSelector(img)
    candSelector.GenerateKMeansCandidates(candNumber, 0.1)
    #save the data
    f = open('E:/GeoVis/weathervis/cand.txt', 'w')
    f.write(str(len(candSelector.candidates)) + "\n")
    for index in candSelector.candidates:
        f.write(str(index['x']) + "\n")
        f.write(str(index['y']) + "\n")
        f.write(str(index['r']) + "\n")
    f.close()
    return HttpResponse('success')

def updateUncertaintyValues(request):
    # load parameters
    #levelNumber = int(request.GET['ln'])
    levelNumber = 4
    
    # load data
    infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
    rootgrp = Dataset(infoPath, format='NETCDF4')
    height = len(rootgrp.dimensions['yf'])
    width = len(rootgrp.dimensions['xf'])
    ens = len(rootgrp.dimensions['ens'])
    variableData = []
    apcp = np.ma.getdata(rootgrp.variables['apcp_fcst_ens'][100][:][:][:])
    variableData.append(apcp)
    rootgrp.close()
    
    # load candidates
    candidatePos = []
    f = open('E:/GeoVis/weathervis/cand.txt', 'r')
    candNumber = int(f.readline())
    for i in range(0, candNumber):
        cand = {}
        cand['x'] = float(f.readline())
        cand['y'] = float(f.readline())
        cand['r'] = float(f.readline())
        candidatePos.append(cand)
    f.close()
    
    unValues = []
    unProcessor = UncertaintyProcessor(ens, height, width, variableData[0])
    # process level 0
    zeroUn = [[0 for x in range(width)] for x in range(height)]
    for y in range(0, height):
        for x in range(0, width):
            zeroUn[y][x] = unProcessor.ProcessUnVolume(x, y, 0)
    unValues.append(zeroUn)
    
    # process level >= 1
    for level in range(1, levelNumber + 1):
        tempValue = [0 for x in range(candNumber)]
        for i in range(0, candNumber):
            tempValue[i] = unProcessor.ProcessUnVolume(candidatePos[i]['x'], candidatePos[i]['y'], level)
        unValues.append(tempValue)
    
    # save uncertainty values
    f = open('E:/GeoVis/weathervis/unValue.txt', 'w')
    f.write(str(levelNumber) + '\n')
    for i in range(height):
        for j in range(width):
            f.write(str(unValues[0][i][j]['mean']) + '\n')
            f.write(str(unValues[0][i][j]['var']) + '\n')
    for level in range(levelNumber):
        for i in range(candNumber):
            f.write(str(unValues[level + 1][i]['mean']) + '\n')
            f.write(str(unValues[level + 1][i]['var']) + '\n')
    f.close()
    
    return HttpResponse('success')
    

def singleLevelOpt(request):
    # load parameters
    alpha = float(request.GET['a'])
    beta = float(request.GET['b'])
    theta = float(request.GET['c'])
    
    # load data
    infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
    rootgrp = Dataset(infoPath, format='NETCDF4')
    height = len(rootgrp.dimensions['yf'])
    width = len(rootgrp.dimensions['xf'])
    ens = len(rootgrp.dimensions['ens'])
    lons_fcst = np.ma.getdata(rootgrp.variables['lons_fcst'][:][:])
    lats_fcst = np.ma.getdata(rootgrp.variables['lats_fcst'][:][:])
    variableData = []
    apcp = np.ma.getdata(rootgrp.variables['apcp_fcst_ens'][100][:][:][:])
    variableData.append(apcp)
    rootgrp.close()
    
    # load candidates
    candidatePos = []
    f = open('E:/GeoVis/weathervis/cand.txt', 'r')
    candNumber = int(f.readline())
    for i in range(0, candNumber):
        cand = {}
        cand['x'] = float(f.readline())
        cand['y'] = float(f.readline())
        cand['r'] = float(f.readline())
        candidatePos.append(cand)
    f.close()
    
    # load uncertainty values
    f = open('E:/GeoVis/weathervis/unValue.txt', 'r')
    levelNumber = int(f.readline())
    unValues = []
    zeroUn = [[0 for x in range(width)] for x in range(height)]
    for i in range(height):
        for j in range(width):
            tempDict = {}
            tempDict['mean'] = float(f.readline())
            tempDict['var'] = float(f.readline())
            zeroUn[i][j] = tempDict
    unValues.append(zeroUn)
    for level in range(levelNumber):
        tempValue = [0 for x in range(candNumber)]
        for i in range(candNumber):
            tempDict = {}
            tempDict['mean'] = float(f.readline())
            tempDict['var'] = float(f.readline())
            tempValue[i] = tempDict
        unValues.append(tempValue)
    f.close()
    
    # solve single level optimization
    levelResult = []
    overlayProc = OverlayProcessor(variableData, candidatePos, unValues)
    overlayProc.setParameters(alpha, beta, theta)
    for level in range(0, levelNumber):
        levelResult.append(overlayProc.heuristicSolve(level + 1))
    
    # save level optimization result
    f = open('E:/GeoVis/weathervis/optresult.txt', 'w')
    f.write(str(levelNumber) + '\n')
    f.write(str(len(levelResult[0])) + '\n')
    for i in range(0, levelNumber):
        for j in range(len(levelResult[i])):
            f.write(str(int(levelResult[i][j])) + '\n')
    f.close()
    
    f = open('E:/GeoVis/weathervis/optresultcons.txt', 'w')
    f.write(str(levelNumber) + '\n')
    f.write(str(len(levelResult[0])) + '\n')
    for i in range(0, levelNumber):
        for j in range(len(levelResult[i])):
            f.write(str(int(levelResult[i][j])) + '\n')
    f.close()
    
    return HttpResponse('success')

def consistencyOpt(request):
    alpha = float(request.GET['a'])
    beta = float(request.GET['b'])
    theta = float(request.GET['c'])
    gamma = float(request.GET['gamma'])
    
    # load data
    infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
    rootgrp = Dataset(infoPath, format='NETCDF4')
    height = len(rootgrp.dimensions['yf'])
    width = len(rootgrp.dimensions['xf'])
    variableData = []
    apcp = np.ma.getdata(rootgrp.variables['apcp_fcst_ens'][100][:][:][:])
    variableData.append(apcp)
    rootgrp.close()
    
    # load candidates
    candidatePos = []
    f = open('E:/GeoVis/weathervis/cand.txt', 'r')
    candNumber = int(f.readline())
    for i in range(0, candNumber):
        cand = {}
        cand['x'] = float(f.readline())
        cand['y'] = float(f.readline())
        cand['r'] = float(f.readline())
        candidatePos.append(cand)
    f.close()
    
    # load uncertainty values
    f = open('E:/GeoVis/weathervis/unValue.txt', 'r')
    levelNumber = int(f.readline())
    unValues = []
    zeroUn = [[0 for x in range(width)] for x in range(height)]
    for i in range(height):
        for j in range(width):
            tempDict = {}
            tempDict['mean'] = float(f.readline())
            tempDict['var'] = float(f.readline())
            zeroUn[i][j] = tempDict
    unValues.append(zeroUn)
    for level in range(levelNumber):
        tempValue = [0 for x in range(candNumber)]
        for i in range(candNumber):
            tempDict = {}
            tempDict['mean'] = float(f.readline())
            tempDict['var'] = float(f.readline())
            tempValue[i] = tempDict
        unValues.append(tempValue)
    f.close()
    
    f = open('E:/GeoVis/weathervis/optresult.txt', 'r')
    levelNumber = int(f.readline())
    siteNumber = int(f.readline())
    levelResult = np.zeros((levelNumber, siteNumber), np.int)
    for i in range(0, levelNumber):
        for j in range(siteNumber):
            levelResult[i][j] = int(f.readline())
    f.close()
    
    consProc = ConsistencyProcessor(candidatePos, levelNumber)
    # update weights
    candWeights = []
    for i in range(levelNumber):
        candWeights.append(consProc.updateLevelData(i + 1, levelResult, gamma))
        
    levelResult = []
    overlayProc = OverlayProcessor(variableData, candidatePos, unValues)
    overlayProc.setParameters(alpha, beta, theta)
    for level in range(0, levelNumber):
        levelResult.append(overlayProc.heuristicSolveWeight(level + 1, candWeights[level]))
        
    # save level optimization result
    f = open('E:/GeoVis/weathervis/optresultcons.txt', 'w')
    f.write(str(levelNumber) + '\n')
    f.write(str(len(levelResult[0])) + '\n')
    for i in range(0, levelNumber):
        for j in range(len(levelResult[i])):
            f.write(str(int(levelResult[i][j])) + '\n')
    f.close()
    
    # single level optimization
    return HttpResponse('success')

def getOptResult(request):
    currentLevel = int(request.GET['level'])
    
    # load data
    infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
    rootgrp = Dataset(infoPath, format='NETCDF4')
    height = len(rootgrp.dimensions['yf'])
    width = len(rootgrp.dimensions['xf'])
    lons_fcst = np.ma.getdata(rootgrp.variables['lons_fcst'][:][:])
    lats_fcst = np.ma.getdata(rootgrp.variables['lats_fcst'][:][:])
    rootgrp.close()
    
    if currentLevel == 0:
        f = open('E:/GeoVis/weathervis/unValue.txt', 'r')
        levelNumber = int(f.readline())
        jsData = []
        nodeCount = 0
        for i in range(height):
            for j in range(width):
                glyphData = {}
                glyphData['r'] = 0.05
                glyphData['lon'] = float(lons_fcst[i][j])
                glyphData['lat'] = float(lats_fcst[i][j])
                jsData.append(glyphData)
                nodeCount += 1
        try:
            json_data = json.dumps(jsData)
        except Exception as ex:
            print ex    
        print nodeCount
        return JsonResponse(json_data, safe=False)
    #load level optimization data
    # load candidates
    candidatePos = []
    f = open('E:/GeoVis/weathervis/cand.txt', 'r')
    candNumber = int(f.readline())
    for i in range(0, candNumber):
        cand = {}
        cand['x'] = float(f.readline())
        cand['y'] = float(f.readline())
        cand['r'] = float(f.readline())
        candidatePos.append(cand)
    f.close()
    
    f = open('E:/GeoVis/weathervis/optresultcons.txt', 'r')
    levelNumber = int(f.readline())
    siteNumber = int(f.readline())
    levelResult = np.zeros((levelNumber, siteNumber), np.int)
    for i in range(0, levelNumber):
        for j in range(siteNumber):
            levelResult[i][j] = int(f.readline())
    f.close()
    if (currentLevel >= levelNumber): currentLevel = levelNumber
    
    jsData = []
    nodeCount = 0
    for i in range(siteNumber):
        if (levelResult[currentLevel - 1][i] == 1):
            glyphData = {}
            r = pow(2, int(i / candNumber))
            if r < candidatePos[i % candNumber]['r']:
                r = candidatePos[i % candNumber]['r']
            glyphData['r'] = r * (lons_fcst[1][2] - lons_fcst[1][1])
            x = int(float(candidatePos[i % candNumber]['x']))
            y = int(float(candidatePos[i % candNumber]['y']))
            glyphData['lon'] = float(lons_fcst[y][x])
            glyphData['lat'] = float(lats_fcst[y][x])
            jsData.append(glyphData)
            nodeCount += 1
    try:
        json_data = json.dumps(jsData)
    except Exception as ex:
        print ex    
    print nodeCount
    return JsonResponse(json_data, safe=False)
    

# def glyphValues(request):
#     #level = Math.round(request.GET['level'])
#     #model = request.GET['model']
#     #variable = request.GET['var']
#     #date = request.GET['date']
#     level = 3
#     infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
#     rootgrp = Dataset(infoPath, format='NETCDF4')
#     xfLen = len(rootgrp.dimensions['xf'])
#     yfLen = len(rootgrp.dimensions['yf'])
#     ensLen = len(rootgrp.dimensions['ens'])
#     lons_fcst = np.ma.getdata(rootgrp.variables['lons_fcst'][:][:])
#     lats_fcst = np.ma.getdata(rootgrp.variables['lats_fcst'][:][:])
#     rootgrp.close()
#     f = open('E:/Data/00_24/apcp_ens/2002010200.apcp', 'rb')
#     dataValues = np.fromfile(f, dtype=np.float32).reshape((ensLen, yfLen, xfLen))
#     f.close()
#     jsData = []
#     xNum = int(round(xfLen / level))
#     yNum = int(round(yfLen / level))
#     meanArray = np.zeros(ensLen)
#     for i in range(0, yNum):
#         for j in range(0, xNum):
#             varMean = 0
#             for k in range(0, ensLen):
#                 meanArray[k] = 0
#                 for bi in range(0, level):
#                     for bj in range(0, level):
#                         meanArray[k] += dataValues[k][i * level + bi][j * level + bj]
#                 meanArray[k] /= (level * level)
#                 varMean += meanArray[k]
#             varMean /= ensLen
#             varVari = 0
#             for k in range(0, ensLen):
#                 varVari += pow(meanArray[k] - varMean, 2)
#             varVari /= ensLen
#             glyphData = {}
#             glyphData['mean'] = varMean
#             glyphData['var'] = varVari
#             glyphData['lon'] = float(lons_fcst[i * level][j * level])
#             glyphData['lat'] = float(lats_fcst[i * level][j * level])
#             jsData.append(glyphData)
#     try:
#         json_data = json.dumps(jsData)
#     except Exception as ex:
#         print ex    
#     return JsonResponse(json_data, safe=False)

# def kmeansValues(request):
#     level = int(request.GET['level'])
#     infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
#     rootgrp = Dataset(infoPath, format='NETCDF4')
#     lons_fcst = np.ma.getdata(rootgrp.variables['lons_fcst'][:][:])
#     lats_fcst = np.ma.getdata(rootgrp.variables['lats_fcst'][:][:])
#     rootgrp.close()
#     
#     img = cv2.imread('E:/Geovis/weathervis/test.png')
#     img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     nodeCluster = NodeCluster()
#     nodeCluster.processImage(img, level * 50)
#     jsData = []
#     for index in nodeCluster.labelIndex:
#         x = round(index['x'])
#         y = round(index['y'])
#         pixelNum = index['nodeNum']
#         glyphData = {}
#         glyphData['r'] = math.sqrt(pixelNum) * (lons_fcst[1][1] - lons_fcst[1][0]) / 3
#         glyphData['lon'] = float(lons_fcst[y][x])
#         glyphData['lat'] = float(lats_fcst[y][x])
#         jsData.append(glyphData)
#     try:
#         json_data = json.dumps(jsData)
#     except Exception as ex:
#         print ex    
#     return JsonResponse(json_data, safe=False)
# 
# def hierarValues(request):
#     level = int(request.GET['level'])
#     infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
#     rootgrp = Dataset(infoPath, format='NETCDF4')
#     lons_fcst = np.ma.getdata(rootgrp.variables['lons_fcst'][:][:])
#     lats_fcst = np.ma.getdata(rootgrp.variables['lats_fcst'][:][:])
#     rootgrp.close()
#     
#     img = cv2.imread('E:/Geovis/weathervis/test.png')
#     img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     test = img[0, 0]
#     nodeCluster = NodeCluster()
#     nodeCluster.processImageHier(img, level * 50)
#     jsData = []
#     for index in nodeCluster.labelIndex:
#         x = round(index['x'])
#         y = round(index['y'])
#         pixelNum = index['nodeNum']
#         glyphData = {}
#         glyphData['r'] = math.sqrt(pixelNum) * (lons_fcst[1][1] - lons_fcst[1][0]) / 3
#         glyphData['lon'] = float(lons_fcst[y][x])
#         glyphData['lat'] = float(lats_fcst[y][x])
#         jsData.append(glyphData)
#     try:
#         json_data = json.dumps(jsData)
#     except Exception as ex:
#         print ex    
#     return JsonResponse(json_data, safe=False)
# 
# def linearOpt(request):
#     level = int(request.GET['level'])
#     alpha = float(request.GET['a'])
#     beta = float(request.GET['b'])
#     theta = float(request.GET['c'])
#     infoPath = 'E:/Data/refcstv2_precip_ccpav2_000_to_024.nc'
#     rootgrp = Dataset(infoPath, format='NETCDF4')
#     lons_fcst = np.ma.getdata(rootgrp.variables['lons_fcst'][:][:])
#     lats_fcst = np.ma.getdata(rootgrp.variables['lats_fcst'][:][:])
#     rootgrp.close()
#     
#     img = cv2.imread('E:/Geovis/weathervis/test.png')
#     img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     test = img[0, 0]
#     nodeCluster = NodeCluster()
#     nodeCluster.processImageHier(img, 200)
#     # update node x y coordinate
#     for index in nodeCluster.labelIndex:
#         x = int(index['x'])
#         y = int(index['y'])
#         index['x'] = lons_fcst[y][x]
#         index['y'] = lats_fcst[y][x]
#     proc = OverlayProcessor(nodeCluster)
#     proc.setCurrentLevel(level)
#     proc.setParameters(alpha, beta, theta)
#     proc.heuristicSolve()
#     jsData = []
#     nodeCount = 0
#     for i in range(0, len(proc.S)):
#         if (proc.z[i] == 1):
#             index = proc.S[i]
#             pixelNum = index['nodeNum']
#             glyphData = {}
#             glyphData['r'] = (index['level']) * 0.2
#             glyphData['lon'] = float(index['x'])
#             glyphData['lat'] = float(index['y'])
#             jsData.append(glyphData)
#             nodeCount += 1
#     try:
#         json_data = json.dumps(jsData)
#     except Exception as ex:
#         print ex    
#     print nodeCount
#     return JsonResponse(json_data, safe=False)
            