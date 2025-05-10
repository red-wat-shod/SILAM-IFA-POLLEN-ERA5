import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, ticker
from matplotlib.animation import FuncAnimation
from netCDF4 import Dataset
import geopandas as gpd
from shapely.geometry import box
import sys
import subprocess
import imageio
import cartopy.crs as ccrs  # Импортируем cartopy

# user parameters #########################################################################
date='202408' #sys.argv[1]
days='31' #sys.argv[2]
netcdf_dir = '../out/'+date # input netcdf file
netcdf_var = 'cnc_POLLEN_RAGWEED_m18' #variable of interest
output_gif = f'pollen_{date}.gif' #output gif file
#output_mp4 = f'pollen_{date}.mp4' #output mp4 file
netcdf_file = f'{netcdf_dir}/pollen_{date}.nc4'
#netcdf_file = f'../out/IFA_SILAM_ERA5_pollen_2024.nc4'
output_gif = f'{netcdf_var}-{date}.gif'
frame_duration = 0.2 #seconds per frame
nodatavalue=9e+36 # will be set to background color
### color scheme
cmap = cm.get_cmap("YlOrRd").copy()
cmap.set_bad('white') #background color
cmap.set_under('white')
vmin=5
vmax=1000
levels = [1, 5, 10, 25,50,100,500,1000,5000]
colors=('silver','palegreen', 'chartreuse', 'yellow','orange','orangered','crimson','darkred')
#levels = np.linspace(vmin, vmax, 11)

# define image properties
width = 400
height = 400
dpi = 50
resolution = '50m'



def read_netcdf_file(netcdf_file):
    with Dataset(netcdf_file, 'r') as dataset:
        data = dataset.variables[netcdf_var][:, 0, : , :]  # параметр 'cnc_POLLEN_BIRCH_m22'
        print(dataset.variables['time'].units)
        startdate=datetime.datetime.strptime(dataset.variables['time'].units, 'seconds since %Y-%m-%d %H:%M:%S %Z')
        times = dataset.variables['time'][:]  # предполагаем, что переменная времени называется 'time'
        lats = dataset.variables['lat'][:]  # предполагаем, что переменная широты называется 'lat'
        lons = dataset.variables['lon'][:]  # предполагаем, что переменная долготы называется 'lon'
    return data, times, lats, lons, startdate

def create_animation(data, times, lats, lons, datetime_vals):
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.AlbersEqualArea(central_longitude=37.6, central_latitude=55.8), position=[0.2,0.2,0.4,0.4] ) #Moscow -- 55.75, 37.616667
    #fig.subplots_adjust(bottom=0.4)
    ax.set_extent([lons.min(), lons.max(), lats.min(), lats.max()])#,crs=ccrs.AlbersEqualArea())
    """
    ax = plt.axes(projection=ccrs.PlateCarree())  # Устанавливаем проекцию
   
    # Замените ax.grid на:
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                        linestyle='--', color='gray', alpha=0.5)
    gl.xlabels_top = False
    gl.ylabels_left = False

    # Добавьте координаты в формате градусов:
    from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    """
    # Выбираем начальный срез данных для отображения
    #im = ax.imshow(data[0], extent=[lons.min(), lons.max(), lats.min(), lats.max()], cmap=cmap, vmin=vmin, vmax=vmax, transform=ccrs.AlbersEqualArea())
    im = ax.contourf(lons, lats, data[0], levels=levels, colors=colors, extend = 'max', transform=ccrs.PlateCarree())#, transform=ccrs.AlbersEqualArea())
    im.cmap.set_over('purple') #background color
    #im.cmap.set_under('white')
    cbar=plt.colorbar(im, location='bottom',fraction=0.03, pad=0.1)#, label=r'$m^{-3}$')
    #cbar.set_ticks(ticks=[ 0, 1000], labels=['0', r'$10^3$'])
    #ax.grid(True, linestyle='--', color='gray', alpha=0.5)  # добавляем координатную сетку
    gl=ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    gl.top_labels = False
    gl.left_labels = False
    ax.annotate('Data source: SILAM running by ERA5\n (c) Vasily Lyulyukin', fontsize=9, xy=(.5, .025), xycoords='figure fraction', horizontalalignment='center', verticalalignment='bottom')
    #ax.set_xlabel('Data source: SILAM running by ERA5\n (c) Vasily Lyulyukin', fontsize=9)
    ax.coastlines()
    ax.axis('off')
    #fig.tight_layout()
    # Загружаем географические данные (например, границы стран)
    #world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    #oastlines = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    #coastlines = coastlines.boundary  # Получаем только границы полигонов


    # Обрезаем географические контуры по границам области данных
    #world_clipped = coastlines.clip(box(minx=lons[0], miny=lats[0], maxx=lons[-1], maxy=lats[-1]))
    #world_clipped.plot(ax=ax, color='none', edgecolor='black', zorder=10)  # отображаем границы стран поверх данных

    def update(frame,im, ax):
        # Обновляем данные для отображения
        for c in im.collections:
            c.remove()  # removes only the contours, leaves the rest intact
        im  = ax.contourf(lons, lats, data[frame], levels=levels, colors=colors, extend = 'max', transform=ccrs.PlateCarree())
        #im.set_array(data[frame])
        #ax.grid(True, linestyle='--', color='gray', alpha=0.5)
        #world_clipped.plot(ax=ax, color='none', edgecolor='black', zorder=10)
        currdate=datetime_vals[frame]
        currdate_fmt = currdate.strftime('%Y-%m-%d %H:%M:%S %Z')
 
        ax.set_title(f'cnc_POLLEN_RAGWEED_m18 {currdate_fmt}', fontsize=12)  # добавляем время
        return im  # возвращаем список с объектом contour    # добавляем координаты

    #ani = FuncAnimation(fig, update, frames=range(len(times)), blit=True)

    # Сохраняем анимацию в формате gif
    #ani.save('animation.gif', writer='pillow')

    # Создаем папку для сохранения отдельных кадров
    if not os.path.exists('frames'):
        os.mkdir('frames')

    # Сохраняем отдельные кадры в формате jpg
    filenames=[]
    for i in range(len(data)):
        filename=f'frames/frame_{i:03d}.png'
        im=update(i, im, ax)  # обновляем график для следующего кадра
        plt.savefig(filename)
        filenames.append(filename)
    plt.show()
    return filenames



def build_gif(filenames, output_gif):
    with imageio.get_writer(output_gif, mode='I',duration=frame_duration) as writer:
        for filename in filenames:
                if os.path.exists(filename):
                    image = imageio.imread(filename)
                    writer.append_data(image)

if __name__ == '__main__':
    subprocess.run(["ncrcat", "-n", f"{days},2,1", f'{netcdf_file[:-4]}01.nc4', netcdf_file])
    #folder_path = '../out/202403'  # замените на путь к вашей папке с файлами NC4
    data,times, lats, lons, startdate = read_netcdf_file(netcdf_file)
    datetime_vals=[(startdate+datetime.timedelta(seconds=float(x))) for x in  times]
    print(np.asarray(times))
    
    filenames = create_animation(data, times, lats, lons, datetime_vals)
    build_gif(filenames, output_gif)

