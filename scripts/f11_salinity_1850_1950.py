# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 11:09:00 2019

@author: Shihan Li
Salinity map
"""
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
#readdata function
from netCDF4 import Dataset
def readdata(file_name):
    file_path_re = r'D:\LifeInBremen\MODULES\Project\data\ocean'
    b = '/'
    file_path = file_path_re + b + file_name
    file_obj = Dataset(file_path)
    print(file_obj.variables.keys())
    return file_obj
def static_plot(time_index, key_variable, lat, lon, 
                figsize, title1, colorbar_title,figtitle):
    #time_index: time interval filter conditions; key_variable: key variables for ploting
    #lat, lon: coordinates from data
    #figsize: define the size of final figure
    #titles: title name for each element respectively
    time_interval = time[time_index] #make the time interval
    #pick up the key variable value for  correspondent time interval
    key_variable_in_interval = key_variable[time_index[0][0]:time_index[0][-1]+1,:,:] 
    #calculate the average in this time interval
    key_variable_ave = np.empty([len(lat),len(lon)])
    for i in range(len(lat)):
        for j in range(len(lon)):
            key_variable_ave[i,j] = np.mean(key_variable_in_interval[:,i,j])
    #calculate zonal average
    key_variable_zonal = np.empty([len(time_interval),len(lat)])
    for i in range(len(time_interval)):
        for j in range(len(lat)):
            key_variable_zonal[i,j] = np.mean(key_variable_in_interval[i,j,:])
    
    upper_limitation = 38
    lower_limitation = 32
    
    #start ploting
    fig = plt.figure(figsize = figsize)

    #plot ax1, average evaporation in last 1kyr
    ax1 = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
    ax1.coastlines()
    #plot ax1.controuf map
    contf = ax1.contourf(lon,lat,key_variable_ave, 
                         levels = np.linspace(lower_limitation, upper_limitation,61),
                         extend = 'both',
                         transform=ccrs.PlateCarree())
    cont = ax1.contour(lon,lat,key_variable_ave, levels = (34,36,37), linewidths =2, 
                       colors = ['0.75','0.85','0.95'],
                  projection=ccrs.PlateCarree())
    ax1.clabel(cont, cont.levels, fmt = '%.0f', fontsize = 20)
    ##contf.cmap.set_under('purple')
    #set title for ax1
    ax1.set_title(title1 , fontweight = 'bold', fontsize = 20)
    #plot the contour line
    #levels = range(100,700,200)
    #countour = ax1.contour(lon, lat, evap_ave, levels = levels, colors='r',linestyles = 'dashed')
    #add colorbar
    cb1 = fig.colorbar(contf, ticks = np.linspace(lower_limitation, upper_limitation,7),  
                       format = '%.1f',
                   orientation = 'horizontal',fraction=0.08, pad=0.12)
    #set ax1.colorbar format
    cb1.set_label(colorbar_title,  fontsize = 16)
    cb1.ax.tick_params(labelsize=16)
    #set ax1 label's and tick's format
    ax1.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
    ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
    ax1.tick_params(axis='both', labelsize=20)
    ax1.xaxis.set_major_formatter(LongitudeFormatter())
    ax1.yaxis.set_major_formatter(LatitudeFormatter())
    ax1.add_feature(cartopy.feature.LAND, zorder=1, edgecolor='black')

    fig.savefig(figtitle)
    return fig

file_name = ('trace.01-36.22000BP.pop.SALT.22000BP_decavg_400BCE.nc')
data_salt = readdata(file_name)
lon = data_salt.variables['TLONG'][:]
lat = data_salt.variables['TLAT'][:]
lat1 = lat[:,0]
time = data_salt.variables['time'][:]
salt = data_salt.variables['SALT'][:,0,:,:] # surface layer
# long_name: Salinity
# units: gram/kilogram



# reorder the sequence of lon and corespondant salt data
lon1 = np.linspace(2.9,359.3,100)
salt_in_lon_sequence = np.float32(np.ma.empty([2204,116,100]))
for i in range(len(time)):
    for j in range(len(lon[1])):
        for k in range(len(lon)):
                if j < 89:
                    salt_in_lon_sequence[i,k,j] = salt[i,k,j+11]
                    #salt_in_lon_sequence[i,k,j].mask = salt[i,k,j+11].mask
                else:
                    salt_in_lon_sequence[i,k,j] = salt[i,k,j-89]
                    #salt_in_lon_sequence[i,k,j].mask = salt[i,k,j-89].mask

            
time_index = np.where(time>=-0.1)
figsize = (12,7)
title1 = 'Salinity (1850-1980 AD)'
colorbar_title = ' g/kg '
figtitle = 'salinity_ave_1850_1980.png'
fig = static_plot(time_index, salt_in_lon_sequence, lat1, lon1, 
                figsize, title1, colorbar_title,figtitle)   




