from netCDF4 import Dataset
from mongoengine import *
import struct

class DataMapType(Document):
    name = StringField(max_length=50).unique
    ens_num = IntField
    lat_begin = FloatField
    lat_step = FloatField
    lat_num = IntField
    lon_begin = FloatField
    lon_step = FloatField
    lon_num = IntField

class DataMapRecord(Document):
    begin_datetime = DateTimeField(required=True)
    forecast_hour = IntField
    ens_id = IntField
    variable_type = StringField(max_length=20)
    binay_value = ListField
    

# import the map type
def import_reforecastv2_map_type(file_name):
    rootgrp = Dataset(file_name, "r")
    temp_ens_num = len(rootgrp.dimensions["ens"])
    temp_lat_num = len(rootgrp.dimensions["lat"])
    temp_lon_num = len(rootgrp.dimensions["lon"])
    lat_values = rootgrp.variables["lat"]
    lon_values = rootgrp.variables["lon"]
    map_type = DataMapType(name = "reforecastv2_china",
                           ens_num = temp_ens_num,
                           lat_begin = lat_values[0],
                           lat_step = lat_values[1] - lat_values[0],
                           lat_num = temp_lat_num,
                           lon_begin = lon_values[0],
                           lon_step = lon_values[1] - lon_values[0],
                           lon_num = temp_lon_num)
    map_type.save()
    print map_type.id
    rootgrp.close()

# import the data
def import_reforecastv2_data(file_name, type):
    rootgrp = Dataset(file_name, "r")
    ens_num = len(rootgrp.dimensions["ens"])
    lat_num = len(rootgrp.dimensions["lat"])
    lon_num = len(rootgrp.dimensions["lon"])
    time_len = len(rootgrp.dimensions["time"])
    fhour_len = len(rootgrp.dimensions["fhour"])
    lat_values = rootgrp.variables["lat"]
    lon_values = rootgrp.variables["lon"]
    ens_values = rootgrp.variables["ens"]
    values = rootgrp.variables["Total_precipitation"]
    time_values = rootgrp.variables["time"]
    f_hour_values = rootgrp.variables["fhour"]
    for t, time in enumerate(time_values):
        for e, ens in enumerate(ens_values):
            for f, f_hour in enumerate(f_hour_values):
                data_map = DataMapRecord(begin_date_time = time,
                                         forcast_hour = f_hour,
                                         ens_id = ens,
                                         variable_type = type,
                                         binary_value = values[t][e][f])
                data_map.save()
    rootgrp.close()
    
# program
import_reforecastv2_data("refcstv2_precip_ccpav2_012_to_024 - Copy.nc", "rain")