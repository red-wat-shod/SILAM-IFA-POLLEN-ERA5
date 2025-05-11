#!/usr/bin/env python

import cdsapi
import os
import subprocess

area = "75.5/26.5/34.5/60.5"
grid = "0.5/0.5"
days = range(1,32)
months=range(3,10)
c = cdsapi.Client()
DIR = os.environ.get('METEO_DIR', '/mnt/DISK_10Tb/ERA5')
for month in months:
    dat='2024-{:02d}'.format(month)
    for day in ["{:02d}".format(x) for x in days]:
        date=f'{dat}-{day}'
        fdate=date.replace('-','')
        target=f'{DIR}/{fdate}/era5-3d-{fdate}.grib'
        fname=target[:-5]+"23.grib"
        if not os.path.exists(fdate): os.makedirs(fdate)
        if not os.path.exists(fname):
            request={
                "class": "ea",
                "date": date,
                "expver": "1",
                "levelist": "61/to/137",
                "levtype": "ml",
                "param": "129/130/131/132/133/135/155/246",
                "stream": "oper",
                "time": "00/to/23/by/1",
                "type": "an",
                "grid": grid,
                "area":area,
                "format":"grib"
                }
            print(request)
            c.retrieve("reanalysis-era5-complete", request, target)
            for hour in range(24):
                fname=target[:-5]+"{:02d}.grib".format(hour)
                subprocess.run(["cdo", "-seltimestep,{:d}".format(hour+1), target, fname])
            subprocess.run(["rm", target])


