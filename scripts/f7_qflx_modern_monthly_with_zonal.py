# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:24:13 2019

@author: Shihan Li
monthly evap in the modern world
"""
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib import animation

#readdata function
from netCDF4 import Dataset
def readdata(file_name):
    file_path_re =r'D:\LifeInBremen\MODULES\Project\data\atmosphere'
    b = '/'
    file_path = file_path_re + b + file_name
    file_obj = Dataset(file_path)
    print(file_obj.variables.keys())
    return file_obj
#read the data
file_name1 = ('trace.36.400BP-1990CE.cam2.h0.QFLX.2160101-2204012.nc')
data_qflx = readdata(file_name1)
qflx = data_qflx.variables['QFLX'][:]
time = data_qflx.variables['time'][:]
lat = data_qflx.variables['lat'][:]
lon = data_qflx.variables['lon'][:]

#water_desnsity constant: 1000kg/m3
water_density = 1000 
#unit conversion constant
unit_conversion_constant = 60 * 60 * 24 *365 * 100
# convert the qflx unit in kg/m2/s to cm/year
qflx = qflx / water_density * unit_conversion_constant

#fulfill the data gap in 360° lon by appending another column in lon and 
#copying the data at 0° to it
lon = np.append(lon, 360)
qflx = np.dstack((qflx,qflx[:,:,0])) 

#define the time interval: 1850 - 1980 AD
time_index = np.where(time>=-0.1)
time_modern = time[time_index]

qflx_modern = qflx[time_index[0][0]:time_index[0][-1]+1,:,:]
month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 
              'Sept', 'Oct', 'Nov', 'Dec']

#calculate the monthly average
qflx_modern_monthly_ave = np.empty([len(month_list),len(lat),len(lon)])
for i in range(len(month_list)):
    qflx_modern_monthly_ave[i,:,:] = np.mean(qflx_modern[i::12,:,:], axis = 0 )

    
#calculate the zonal
qflx_modern_monthly_zonal = np.mean(qflx_modern_monthly_ave, axis = 2)
qflx_modern_annual_zonal = np.mean(qflx_modern_monthly_zonal, axis = 0)

upper_limitation = 300
lower_limitation = 20
######### plot ##############
fig = plt.figure(figsize = (15,6))
grid = plt.GridSpec(1, 3, wspace=0.5, hspace=0.5)
#grid space to place figures

#basemap
ax1 = fig.add_subplot(grid[0,:2], projection=ccrs.PlateCarree())
ax1.coastlines()
#draw controuf map

contf1 = ax1.contourf(lon,lat,qflx_modern_monthly_ave[0,:,:],
                      levels = np.linspace(lower_limitation,upper_limitation,51),
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
ax2 = fig.add_subplot(grid[0,2])
month = month_list[0]
ax2.plot(qflx_modern_monthly_zonal[0,:], lat, linewidth=3.0, 
         #color = 'b', 
         linestyle = '-', label=f'{month}')
ax2.plot(qflx_modern_annual_zonal, lat, linewidth=2.0, 
         #color = 'b', 
         linestyle = '--', label='Annual')
#set ax2 format
ax2.set_ylabel('°N',fontsize = 16)
ax2.tick_params(labelsize=16) 
ax2.set_xlabel("cm/year",fontsize = 16)
ax2.set_xlim([0,200])
ax2.legend(fontsize = 12)

def animate(i): 
    ax1.clear()
    ax2.clear()
    ax1.coastlines(resolution='50m')
    #plot ax1.controuf map
    contf1 = ax1.contourf(lon,lat,qflx_modern_monthly_ave[i,:,:], 
                      levels = np.linspace(lower_limitation,upper_limitation,51),
                      extend = 'both',
                      projection=ccrs.PlateCarree())
    #set title for ax1
    ax1.set_title(f'Evaporation rate({month_list[i]}, 1850-1980 AD)', 
                  fontweight = 'bold', fontsize = 20)
    
   
    #set ax1 label's and tick's format
    ax1.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
    ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
    ax1.tick_params(axis='both', labelsize=20)
    ax1.xaxis.set_major_formatter(LongitudeFormatter())
    ax1.yaxis.set_major_formatter(LatitudeFormatter())
    #plot ax2, average djf precipitation difference

    ax2.plot(qflx_modern_monthly_zonal[i,:], lat, linewidth=3.0, 
         color = 'b', 
         linestyle = '--', label=f'{month_list[i]}')
    ax2.plot(qflx_modern_annual_zonal, lat, linewidth=2.0, 
         color = 'r', 
         linestyle = '-', label='Annual')
    #set ax2 format
    ax2.set_ylabel('°N',fontsize = 16)
    ax2.tick_params(labelsize=16) 
    ax2.set_xlabel("cm/year",fontsize = 16)
    ax2.set_xlim([0,200])
    ax2.legend(fontsize = 12)
    
anim = animation.FuncAnimation(fig, animate, frames=len(month_list), interval=800, blit=False)
anim.save('qflx_modern_monthly_with_zonal.gif', writer='imagemagick')
    


