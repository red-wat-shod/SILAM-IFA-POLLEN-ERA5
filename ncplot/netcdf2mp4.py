# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 16:22:57 2021

@author: Johannes H. Uhl, University of Colorado Boulder, USA.

Modified by Vasily Lyulyukin (Obukhov IAPh RAS) for daily SILAM POLLEN data
"""

import os,sys
import subprocess
import numpy as np
import datetime
from matplotlib import pyplot as plt
from osgeo import gdal
import imageio
#import ffmpy
import moviepy.editor as mp
import matplotlib
#matplotlib.rcParams['font.sans-serif'] = "Arial"
#matplotlib.rcParams['font.family'] = "sans-serif"
plt.rcParams['figure.autolayout'] = True

# user parameters #########################################################################
date=sys.argv[1]
days=sys.argv[2]
netcdf_dir = '../out/'+date # input netcdf file
netcdf_var = 'cnc_POLLEN_BIRCH_m22' #variable of interest
output_gif = f'pollen_{date}.gif' #output gif file
output_mp4 = f'pollen_{date}.mp4' #output mp4 file
netcdf_file = f'{netcdf_dir}/pollen_{date}.nc4'
subprocess.run(["ncrcat", "-n", f"{days},2,1", f'{netcdf_file[:-4]}01.nc4', netcdf_file])

frame_duration = 0.2 #seconds per frame
nodatavalue=9e+36 # will be set to background color
### color scheme
cmap = matplotlib.cm.get_cmap("turbo").copy()
cmap.set_bad('black') #background color
vmin=0
vmax=1000

##########################################################################################

### open netcdf file as array
infile='NETCDF:"'+netcdf_file+'":%s' %(netcdf_var)

ds=gdal.Open(infile)
arr=ds.ReadAsArray()

### get dates
timevalues=ds.GetMetadata()['NETCDF_DIM_time_VALUES'][1:-1].split(',')
timevalues=[int(x) for x in timevalues]
print(timevalues)
startdate = datetime.datetime.strptime(date, "%Y%m")
datetime_vals=[(startdate+datetime.timedelta(seconds=x)) for x in  timevalues]
print(datetime_vals)
### plot each frame to a temporary png image file
filenames = []
epochs=len(timevalues)
for t in np.arange(0,epochs):
    currarr=arr[t,:,:]    
    currarr[currarr>nodatavalue]=-np.nan  ### set no data value to nan
    currdate=datetime_vals[t]
    
    ### select a temporal subset
    #if not currdate.month in [2,4,6,8,10,12]:
    #    continue
    
    ### format the date for plotting and file names:
    currdate_fmt = '%s%s%s%s' %(currdate.year,str(currdate.month).zfill(2),str(currdate.day).zfill(2),str(currdate.hour).zfill(2))
    currdate_fmt2 = '2024-%s-%s' %(str(currdate.month).zfill(2),str(currdate.day).zfill(2))
    
    ### set up plot
    fig,ax=plt.subplots(figsize=(5,5)) ##adjust image aspect to your data
    img=ax.imshow(currarr,cmap=cmap,vmin=vmin,vmax=vmax) ##adjust vmin and vmax to your data
    ax.set_xticks([])
    ax.set_yticks([])
    
    ### add some text:
    ax.set_xlabel('Data source: SILAM running by ERA5\n (c) Vasily Lyulyukin.', fontsize=9)
    ax.set_title(netcdf_var + '\n'+currdate_fmt2, fontsize=15)

    ### customize color bar:
    cbar = fig.colorbar(img,fraction=0.02)
    cbar.set_ticklabels(['{0:+}'.format(int(xx)) if xx!=0 else int(xx) for xx in cbar.ax.get_yticks()]) ## add sign to colorbar ticks
    #from : https://stackoverflow.com/questions/19219963/align-ticklabels-in-matplotlib-colorbar
    ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(ticklabs,ha='right')
    cbar.ax.yaxis.set_tick_params(pad=20)

    ### set edges to white:
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    #plt.show() ### uncomment for testing
    
    ### save frame to png
    filename = '%s.png' %currdate_fmt
    fig.tight_layout(pad=0) #possibly unnecessary as we set rcparams
    fig.savefig(filename,pad_inches = 0) #pad_inches is possibly unnecessary as we set rcparams
    plt.close()
    filenames.append(filename) 
    print(currdate_fmt)
    
    ### uncomment to test a few frames:
    # if t>20:
    #     break
    
# build gif
with imageio.get_writer(output_gif, mode='I',duration=frame_duration) as writer:
    for filename in filenames:
        if os.path.exists(filename):
            image = imageio.imread(filename)
            writer.append_data(image)

# Remove temporary files
for filename in set(filenames):
    if os.path.exists(filename):
        os.remove(filename)
#os.remove(netcdf_file)
# convert to mp4
#clip = mp.VideoFileClip(output_gif)
#clip.write_videofile(output_mp4)

