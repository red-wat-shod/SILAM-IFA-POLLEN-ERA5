#!/usr/bin/env python
import os
import cdsapi
import subprocess

DIR = os.environ.get('METEO_DIR', '/mnt/DISK_10Tb/ERA5')

var=[
        "2m_temperature",
        "2m_dewpoint_temperature",

        "mean_sea_level_pressure",
        "surface_pressure",

        "10m_u_component_of_wind",
        "10m_v_component_of_wind",

        "surface_latent_heat_flux",
        "surface_net_solar_radiation",
        "surface_sensible_heat_flux",
        "top_net_solar_radiation",
        "uv_visible_albedo_for_direct_radiation",

        "high_cloud_cover",
        "low_cloud_cover",
        "medium_cloud_cover",
        "total_cloud_cover",

        #"mean_runoff_rate",
        "runoff",
        "surface_runoff",
        "total_precipitation",
        #"convective_snowfall_rate_water_equivalent",
        "large_scale_rain_rate",
        "large_scale_snowfall_rate_water_equivalent",
        "snow_density",
        "snow_depth",
        "snowfall",
        "large_scale_precipitation",
        
        "temperature_of_snow_layer",
        "soil_temperature_level_1",
        
        "zero_degree_level", 
        "boundary_layer_height",
        #"convective_available_potential_energy",
        #"convective_inhibition",
        "sea_ice_cover",
        "forecast_surface_roughness"
        ]

dataset = "reanalysis-era5-single-levels"
area = [75.5, 26.5, 34.5, 60.5]
grid = [0.5, 0.5]
days = [31]
months=[5,7,8]
client = cdsapi.Client()

for month in months:
    dat='2024{:02d}'.format(month)
    for day in ["{:02d}".format(x) for x in days]:
        fdate=dat+day
        target=f'{DIR}/{fdate}/era5-singl-{fdate}.grib'
        fname=target[:-5]+"23.grib"
        if not os.path.exists(fdate): os.makedirs(fdate)
        if not os.path.exists(fname):
            request = {
                "product_type": ["reanalysis"],
                "variable": var,
                "year": ["2024"],
                "month": ["{:2d}".format(month)],
                "day": [day],
                "time": [
                    "00:00", "01:00", "02:00",
                    "03:00", "04:00", "05:00",
                    "06:00", "07:00", "08:00",
                    "09:00", "10:00", "11:00",
                    "12:00", "13:00", "14:00",
                    "15:00", "16:00", "17:00",
                    "18:00", "19:00", "20:00",
                    "21:00", "22:00", "23:00"
                    ],
                "data_format": "grib",
                "download_format": "unarchived",
                'area': area,
                'grid': grid
                }
            print(request)
            client.retrieve(dataset, request, target)
            for hour in range(24):
                fname=target[:-5]+"{:02d}.grib".format(hour)
                subprocess.run(["cdo", "-seltimestep,{:d}".format(hour+1), target, fname])
            subprocess.run(["rm", target])


