#!/usr/bin/env python
import cdsapi
import os

DIR = os.environ.get('METEO_DIR', '/mnt/DISK_10Tb/ERA5')

area = "75.5/26.5/34.5/60.5"


dataset = "reanalysis-era5-complete"
request = {
    "class": "ea",
    "date": "2024-03-01",
    "expver": "1",
    "levtype": "sfc",
    "param": "27.128/28.128/29.128/30.128/31.128/43.128/129.128/14.228/26.128/244.128/172.128",
    #"param": "173",
    "stream": "oper",
    "time": "00:00:00",
    "type": "an",
    "area": area,
    'grid':"0.5/0.5",
    'data_format':'grib'
}

client = cdsapi.Client()
client.retrieve(dataset, request, f'{DIR}/era5-inv.grib')
