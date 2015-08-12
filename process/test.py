import unextractor
import numpy
from netCDF4 import Dataset
import array
import scipy
import scipy.misc
from overlayprocessing import *
from skimage import data, io, segmentation, color
from skimage.future import graph
from matplotlib import pyplot as plt
import cv2

#unextractor.extractUncertainty('E:/Data/00_24/apcp_ens/2002010200.apcp', 11, 128, 61)
# level = 1
# infoPath = 'E:/Data/00_24/info.nc'
# rootgrp = Dataset(infoPath, format='NETCDF4')
# xfLen = len(rootgrp.dimensions['xf'])
# yfLen = len(rootgrp.dimensions['yf'])
# ensLen = len(rootgrp.dimensions['ens'])
# lons_fcst = rootgrp.variables['lons_fcst'][:][:]
# lats_fcst = rootgrp.variables['lats_fcst'][:][:]
# rootgrp.close()
# file = open('E:/Data/00_24/apcp_ens/2002010200.apcp', 'rb')
# dataValues = numpy.fromfile(file, dtype=numpy.float32)
# dataValues = dataValues.reshape((ensLen, yfLen, xfLen))
# file.close()
# pngMap = numpy.zeros((yfLen, xfLen), numpy.uint8)
# for i in range(0, yfLen):
#     for j in range(0, xfLen):
#         pngMap[i][j] = numpy.uint8(dataValues[0][i][j] * 8)
# scipy.misc.imsave('test.png', pngMap)
