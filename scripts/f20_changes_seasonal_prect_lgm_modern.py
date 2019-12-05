# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 15:31:51 2019

@author: Shihan Li
plot changes of seasonal precipitation difference between LGM and the modern world
"""


import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib import animation
import cmocean
#readdata function
from netCDF4 import Dataset
def readdata(file_name):
    file_path_re = r'D:\LifeInBremen\MODULES\Project\data\atmosphere'
    b = '/'
    file_path = file_path_re + b + file_name
    file_obj = Dataset(file_path)
    print(file_obj.variables.keys())
    return file_obj

#read data from files respectively
file_name_jja = ('trace.01-36.22000BP.cam2.PRECT.22000BP_decavgJJA_400BCE.nc')
file_name_djf = ('trace.01-36.22000BP.cam2.PRECT.22000BP_decavgDJF_400BCE.nc')
data_prect_jja = readdata(file_name_jja)
data_prect_djf = readdata(file_name_djf)
lon = data_prect_jja.variables['lon'][:]
lat = data_prect_jja.variables['lat'][:]
time = data_prect_jja.variables['time'][:]
#unit conversion constant
unit_conversion_constant = 60 * 60 * 24 *365 * 100
# convert unit from m/s to cm/year
prect_jja = data_prect_jja.variables['PRECT'][:]* unit_conversion_constant
prect_djf = data_prect_djf.variables['PRECT'][:]* unit_conversion_constant

#fill up the empty line in the middle
lon = np.append(lon, 360)
prect_jja = np.dstack((prect_jja,prect_jja[:,:,0])) 
prect_djf = np.dstack((prect_djf,prect_djf[:,:,0])) 

#define the time interval: 1850 - 1980 AD
time_index = np.where(time>=-0.1)
time_interval = time[time_index]

prect_jja_interval = prect_jja[time_index[0][0]:time_index[0][-1]+1,:,:]
prect_djf_interval = prect_djf[time_index[0][0]:time_index[0][-1]+1,:,:]

#calculate the average in this time interval
prect_jja_interval_ave = np.empty([len(lat),len(lon)])
prect_djf_interval_ave = np.empty([len(lat),len(lon)])
for i in range(len(lat)):
    for j in range(len(lon)):
        prect_jja_interval_ave[i,j] = np.mean(prect_jja_interval[:,i,j])
        prect_djf_interval_ave[i,j] = np.mean(prect_djf_interval[:,i,j])
        
#calculate zonal average
prect_jja_modern_zonal = np.mean(prect_jja_interval_ave, axis = 1)
prect_djf_modern_zonal = np.mean(prect_djf_interval_ave, axis = 1)
prect_zonal_seasonal_difference_morden = prect_jja_modern_zonal- prect_djf_modern_zonal

#calculate the data for LGM
time_index_lgm = np.where((time>=-22)&(time<=-20))
time_lgm = -time[time_index_lgm]

prect_jja_lgm = prect_jja[time_index_lgm[0][0]:time_index_lgm[0][-1]+1,:,:]
prect_djf_lgm = prect_djf[time_index_lgm[0][0]:time_index_lgm[0][-1]+1,:,:]

#calculate the average in this time interval
prect_jja_lgm_ave = np.empty([len(lat),len(lon)])
prect_djf_lgm_ave = np.empty([len(lat),len(lon)])
for i in range(len(lat)):
    for j in range(len(lon)):
        prect_jja_lgm_ave[i,j] = np.mean(prect_jja_lgm[:,i,j])
        prect_djf_lgm_ave[i,j] = np.mean(prect_djf_lgm[:,i,j])

#calculate zonal average
prect_jja_lgm_zonal = np.empty([len(time_lgm),len(lat)])
prect_djf_lgm_zonal = np.empty([len(time_lgm),len(lat)])
for i in range(len(time_lgm)):
         prect_jja_lgm_zonal[i,:] = np.mean(prect_jja_lgm[i,:,:], axis = 1)
         prect_djf_lgm_zonal[i,:] = np.mean(prect_djf_lgm[i,:,:], axis = 1)
         
prect_jja_lgm_modern_difference = prect_jja_lgm - prect_jja_interval_ave
prect_djf_lgm_modern_difference = prect_djf_lgm - prect_djf_interval_ave
prect_lgm_zonal_seasonal_difference = prect_jja_lgm_zonal - prect_djf_lgm_zonal
prect_changes_seasonal_prect_diff = abs(prect_jja_lgm - prect_djf_lgm) - abs((prect_jja_interval_ave- prect_djf_interval_ave))

upper_limitation = 180
lower_limitation = -180

## plot
fig = plt.figure(figsize = (10,7))

#basemap
ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
ax1.coastlines()
#draw controuf map
contf1 = ax1.contourf(lon,lat,prect_changes_seasonal_prect_diff[0,:,:],
                      levels = np.linspace(lower_limitation,upper_limitation,61),
                      extend = 'both',
                      cmap = cmocean.cm.balance,
                      projection=ccrs.PlateCarree())
#add colorbar
cb1 = fig.colorbar(contf1, ticks = np.linspace(lower_limitation, upper_limitation, 11),  
                   format = '%.0f',
                   orientation = 'horizontal',fraction=0.08, pad=0.15)
#set colorbar format
cb1.set_label('cm/year', fontsize = 16)
cb1.ax.tick_params(labelsize=16)
#set ax1 label's and tick's format
ax1.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
ax1.tick_params(axis='both', labelsize=20)
ax1.xaxis.set_major_formatter(LongitudeFormatter())
ax1.yaxis.set_major_formatter(LatitudeFormatter())

def animate(i): 
    ax1.clear()
    ax1.coastlines(resolution='50m')
    #plot ax1.controuf map
    contf1 = ax1.contourf(lon,lat,prect_changes_seasonal_prect_diff[i*5,:,:], 
                      levels = np.linspace(lower_limitation,upper_limitation,61),
                      cmap = cmocean.cm.balance,
                      extend = 'both',
                      projection=ccrs.PlateCarree())
    #set title for ax1
    ax1.set_title('''Changes of seasonal precipitation difference
from the modern world (%.2f ka BP)''' %time_lgm[i*5],
                  fontweight = 'bold', fontsize = 20)
    
   
    #set ax1 label's and tick's format
    ax1.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
    ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
    ax1.tick_params(axis='both', labelsize=20)
    ax1.xaxis.set_major_formatter(LongitudeFormatter())
    ax1.yaxis.set_major_formatter(LatitudeFormatter())

anim = animation.FuncAnimation(fig, animate, frames=len(time_lgm)//5, interval=800,blit=False)
anim.save('changes_prect_seasonal_lgm_modern_difference_with_zonal.gif', writer='imagemagick')