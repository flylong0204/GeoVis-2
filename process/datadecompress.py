from netCDF4 import Dataset
from lib2to3.fixer_util import String
import os

rootgrp = Dataset('E:/Data/refcstv2_precip_ccpav2_000_to_024.nc', format='NETCDF4')

# Load data from the big file and save as small files for each day
# Separate variables
xaLen = len(rootgrp.dimensions['xa'])
yaLen = len(rootgrp.dimensions['ya'])
xfLen = len(rootgrp.dimensions['xf'])
yfLen = len(rootgrp.dimensions['yf'])
ensLen = len(rootgrp.dimensions['ens'])
timeLen = len(rootgrp.dimensions['time'])

folderName = 'E:/Data/00_24'

infoFile = folderName + '/info.nc'
infoGroup = Dataset(infoFile, 'w')
infoGroup.createDimension('xa', xaLen)
infoGroup.createDimension('ya', yaLen)
infoGroup.createDimension('xf', xfLen)
infoGroup.createDimension('yf', yfLen)
infoGroup.createDimension('ens', ensLen)
infoGroup.createDimension('time', timeLen)
infoGroup.createVariable('lons_anal', 'f4', ('ya', 'xa',))
infoGroup.createVariable('lats_anal', 'f4', ('ya', 'xa',))
infoGroup.createVariable('lons_fcst', 'f4', ('yf', 'xf',))
infoGroup.createVariable('lats_fcst', 'f4', ('yf', 'xf',))
infoGroup.createVariable('init_time', 'int32', ('time',))
infoGroup.variables['lons_anal'][:][:] = rootgrp.variables['lons_anal'][:][:]
infoGroup.variables['lats_anal'][:][:] = rootgrp.variables['lats_anal'][:][:]
infoGroup.variables['lons_fcst'][:][:] = rootgrp.variables['lons_fcst'][:][:]
infoGroup.variables['lats_fcst'][:][:] = rootgrp.variables['lats_fcst'][:][:]
infoGroup.variables['init_time'][:] = rootgrp.variables['yyyymmddhh_init'][:]
temp = infoGroup.variables['init_time'][:]
infoGroup.close()
 

# save header information

initTimes = rootgrp.variables['yyyymmddhh_init'][:]
# save precipitation data
pFolderName = folderName + '/apcp_ens/'
apcpFcst = rootgrp.variables['apcp_fcst_ens']
if not os.path.exists(pFolderName):
    os.makedirs(pFolderName)
index = 0
for t in initTimes:
    tempFileName = pFolderName + str(t) + '.apcp'
    f = open(tempFileName, 'wb')
    tempData = apcpFcst[index][:][:][:]
    index += 1
    f.write(tempData)
    f.close()

# save precipitation analysis
pFolderName = folderName + '/apcp_anal/'
apcpAnal = rootgrp.variables['apcp_anal']
if not os.path.exists(pFolderName):
    os.makedirs(pFolderName)
index = 0
for t in initTimes:
    tempFileName = pFolderName + str(t) + '.anal'
    f = open(tempFileName, 'wb')
    tempData = apcpAnal[index][:][:]
    index += 1
    f.write(tempData)
    f.close()
    
# precipitable water
pFolderName = folderName + '/prew_mean/'
varValues = rootgrp.variables['pwat_fcst_mean']
if not os.path.exists(pFolderName):
    os.makedirs(pFolderName)
index = 0
for t in initTimes:
    tempFileName = pFolderName + str(t) + '.prew'
    f = open(tempFileName, 'wb')
    tempData = varValues[index][:][:]
    index += 1
    f.write(tempData)
    f.close()

pFolderName = folderName + '/t2m_mean/'
varValues = rootgrp.variables['T2m_fcst_mean']
if not os.path.exists(pFolderName):
    os.makedirs(pFolderName)
index = 0
for t in initTimes:
    tempFileName = pFolderName + str(t) + '.t2m'
    f = open(tempFileName, 'wb')
    tempData = varValues[index][:][:]
    index += 1
    f.write(tempData)
    f.close()
    
pFolderName = folderName + '/mslp_mean/'
varValues = rootgrp.variables['MSLP_fcst_mean']
if not os.path.exists(pFolderName):
    os.makedirs(pFolderName)
index = 0
for t in initTimes:
    tempFileName = pFolderName + str(t) + '.mslp'
    f = open(tempFileName, 'wb')
    tempData = varValues[index][:][:]
    index += 1
    f.write(tempData)
    f.close()

rootgrp.close()