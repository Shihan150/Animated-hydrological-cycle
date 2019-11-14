# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 16:36:20 2019

@author: Shihan Li
plot evaporation for last 1kyr
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

#readdata function
from netCDF4 import Dataset
def readdata(file_name):
    file_path_re = r'C:\Users\59506\Desktop\plot\atmosphere'
    b = '/'
    file_path = file_path_re + b + file_name
    file_obj = Dataset(file_path)
    print(file_obj.variables.keys())
    return file_obj

##read precipitation data
file_name1 = ('trace.01-36.22000BP.cam2.QFLX.22000BP_decavg_400BCE.nc')
data_qflx = readdata(file_name1)
lon = data_qflx.variables['lon'][:]
lat = data_qflx.variables['lat'][:]
time = data_qflx.variables['time'][:]
#unit conversion constant
unit_conversion_constant = 60 * 60 * 24 *365 * 100
water_density = 1000
# convert unit from m/s to cm/year
qflx = data_qflx.variables['QFLX'][:]* unit_conversion_constant/water_density

#fulfill the data gap in 360° lon by appending another column in lon and 
#copying the data at 0° to it
lon = np.append(lon, 360)
qflx = np.dstack((qflx,qflx[:,:,0])) 

#define the time interval: 850 - 1850 AD
time_index = np.where((time>=-1.1)&(time<=-0.1))
time_last_1kyr = time[time_index]

qflx_last_1kyr = qflx[time_index[0][0]:time_index[0][-1]+1,:,:]



#calculate the average in this time interval
qflx_ave = np.empty([len(lat),len(lon)])
for i in range(len(lat)):
    for j in range(len(lon)):
        mean = np.mean(qflx_last_1kyr[:,i,j])
        qflx_ave[i,j] = mean

#calculate zonal average
qflx_zonal = np.empty([len(time_last_1kyr),len(lat)])
for i in range(len(time_last_1kyr)):
    for j in range(len(lat)):
        mean = np.mean(qflx_last_1kyr[i,j,:])
        qflx_zonal[i,j] = mean        
        
# calculate 1850-1980 AD as comparison
time_index2 = np.where(time>=-0.1)
time_interval2 = time[time_index2] #make the time interval
    #pick up the key variable value for  correspondent time interval
qflx_1850_1980 = qflx[time_index2[0][0]:time_index2[0][-1]+1,:,:] 
    #calculate the average in this time interval
qflx_1850_1980_ave = np.empty([len(lat),len(lon)])
for i in range(len(lat)):
    for j in range(len(lon)):
        qflx_1850_1980_ave[i,j] = np.mean(qflx_1850_1980[:,i,j])
    #calculate zonal average
qflx_1850_1980_zonal = np.mean(qflx_1850_1980_ave,axis = 1)

upper_limitation = 20
lower_limitation = -40

## plot

fig = plt.figure(figsize = (12,14))
#grid space to place figures

#basemap
ax1 = fig.add_subplot(211, projection=ccrs.PlateCarree())
ax1.coastlines()
#draw controuf map
contf1 = ax1.contourf(lon,lat,qflx_last_1kyr[0,:,:]-qflx_1850_1980_ave,
                      levels = np.linspace(lower_limitation,upper_limitation,61),
                      extend = 'both',
                      projection=ccrs.PlateCarree())
#add colorbar
cb1 = fig.colorbar(contf1, ticks = np.linspace(lower_limitation,upper_limitation,11),  
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

##plot ax2, temporal change of zonal average evaporation
ax2 = fig.add_subplot(212)
t = 1950 + time_last_1kyr[0]*1000
ax2.plot(lat, qflx_zonal[0,:], linewidth=3.0, color = 'b', label='%.0f AD' %t)
ax2.plot(lat, qflx_1850_1980_zonal, linewidth = 3.0, color = 'r',   linestyle = '--', label = '1850-1980 AD')
#set ax2 format
ax2.set_xlabel('°N',fontsize = 16)
ax2.tick_params(labelsize=16) 
ax2.set_ylabel("cm/year",fontsize = 16)
ax2.set_ylim([0,np.max(qflx_zonal)+40])
ax2.legend(fontsize = 20)

#animate the plot with temporal change
def animate(i): 
    ax1.clear()
    ax2.clear()
    contf1 = ax1.contourf(lon,lat,qflx_last_1kyr[i*5,:,:]-qflx_1850_1980_ave,
                          levels = np.linspace(lower_limitation,upper_limitation,61), 
                          extend = 'both',
                          projection=ccrs.PlateCarree())
    ax1.coastlines()
    t = 1950 + time_last_1kyr[i*5]*1000
    ax1.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
    ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
    ax1.tick_params(axis='both', labelsize=20)
    ax1.xaxis.set_major_formatter(LongitudeFormatter())
    ax1.yaxis.set_major_formatter(LatitudeFormatter())
    ax2.plot(lat, qflx_zonal[i*5,:],linewidth=3.0, color = 'b', linestyle = '--', label='%.0f AD' %t)
    ax2.plot(lat, qflx_1850_1980_zonal, linewidth = 2.0, color = 'r', 
             label = '1850-1980 AD')
    ax2.set_ylim([0,175])
    ax2.legend(fontsize = 20)
    ax2.set_xlabel('°N',fontsize = 16)
    ax2.set_ylim([0,np.max(qflx_zonal)+40])
    ax2.tick_params(labelsize=16) 
    ax2.set_ylabel("cm/year",fontsize = 16)
    ax1.set_title('Evaporation diffrence from the modern world (%.0f AD)' %t, fontweight = 'bold', fontsize = 20  )
    ax2.set_title('Zonal average evaporation rate (%.0f AD)' %t,fontweight = 'bold', fontsize = 20 )
    #plt.suptitle('%.2f ka BP' %t,fontsize = 30, y=0.92)
     
    
anim = animation.FuncAnimation(fig, animate, frames=len(time_last_1kyr)//5, interval=800,blit=False)
anim.save('qflx_diff_last_1ka_with_zonal.gif', writer='imagemagick')
