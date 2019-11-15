# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 14:13:39 2019

@author: Shihan Li
annual and seasonal evaporation difference
"""
#import needed package
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

#readdata function
from netCDF4 import Dataset
def readdata(file_name):
    file_path_re = r'D:\LifeInBremen\MODULES\Project\data\atmosphere'
    b = '/'
    file_path = file_path_re + b + file_name
    file_obj = Dataset(file_path)
    print(file_obj.variables.keys())
    return file_obj

#read and process the annual evap data
file_name_qflx = ('trace.01-36.22000BP.cam2.QFLX.22000BP_decavg_400BCE.nc')
data_qflx = readdata(file_name_qflx)
qflx = data_qflx.variables['QFLX'][:]
lon = data_qflx.variables['lon'][:]
lat = data_qflx.variables['lat'][:]
time = data_qflx.variables['time'][:]

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
time_interval = time[time_index]
qflx_interval = qflx[time_index[0][0]:time_index[0][-1]+1,:,:]


#calculate the average in this time interval
qflx_interval_ave = np.empty([len(lat),len(lon)])
for i in range(len(lat)):
    for j in range(len(lon)):
        qflx_interval_ave[i,j] = np.mean(qflx_interval[:,i,j])
        

#calculate zonal average
qflx_zonal = np.mean(qflx_interval_ave, axis = 1)
               
#read and analyze the seasonal evap data
file_name_jja = ('trace.01-36.22000BP.cam2.QFLX.22000BP_decavgJJA_400BCE.nc')
file_name_djf = ('trace.01-36.22000BP.cam2.QFLX.22000BP_decavgDJF_400BCE.nc')
#read data from files respectively
data_qflx_jja = readdata(file_name_jja)
data_qflx_djf = readdata(file_name_djf)

# convert unit from m/s to cm/year
qflx_jja = data_qflx_jja.variables['QFLX'][:]/ water_density* unit_conversion_constant
qflx_djf = data_qflx_djf.variables['QFLX'][:]/ water_density* unit_conversion_constant

#fill up the empty line in the middle
qflx_jja = np.dstack((qflx_jja,qflx_jja[:,:,0])) 
qflx_djf = np.dstack((qflx_djf,qflx_djf[:,:,0])) 

qflx_jja_interval = qflx_jja[time_index[0][0]:time_index[0][-1]+1,:,:]
qflx_djf_interval = qflx_djf[time_index[0][0]:time_index[0][-1]+1,:,:]

#calculate the average in this time interval
qflx_jja_interval_ave = np.empty([len(lat),len(lon)])
qflx_djf_interval_ave = np.empty([len(lat),len(lon)])
for i in range(len(lat)):
    for j in range(len(lon)):
        qflx_jja_interval_ave[i,j] = np.mean(qflx_jja_interval[:,i,j])
        qflx_djf_interval_ave[i,j] = np.mean(qflx_djf_interval[:,i,j])
        
#calculate zonal average
qflx_jja_zonal = np.mean(qflx_jja_interval_ave, axis = 1)
qflx_djf_zonal = np.mean(qflx_djf_interval_ave, axis = 1)

#define the value range for contourf map
upper_limitation = 300
lower_limitation = 20

#####-------------------------------------------------------------------##########

#plot the figure
fig = plt.figure(figsize = (30,15))

#plot ax1, annual evap in 1850-1980
ax1 = fig.add_subplot(2,2,3, projection=ccrs.PlateCarree())
ax1.coastlines()
#plot ax1.controuf map
contf1 = ax1.contourf(lon,lat,qflx_interval_ave, 
                      levels = np.linspace(lower_limitation,upper_limitation,51),
                      extend = 'both',
                      projection=ccrs.PlateCarree())
#set title for ax1
ax1.set_title('c. Annual evaporation (1850-1980 AD)', fontweight = 'bold', fontsize = 20)

#add colorbar
cb1 = fig.colorbar(contf1, ticks = np.linspace(lower_limitation,upper_limitation,11),  format = '%.0f',
                   orientation = 'horizontal',fraction=0.08, pad=0.1)
#set ax1.colorbar format
cb1.set_label('cm/year',  fontsize = 16)
cb1.ax.tick_params(labelsize=16)
#set ax1 label's and tick's format
ax1.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
ax1.tick_params(axis='both', labelsize=20)
ax1.xaxis.set_major_formatter(LongitudeFormatter())
ax1.yaxis.set_major_formatter(LatitudeFormatter())

#plot ax2, zonal average evaporation in 1850-1980
ax2 = fig.add_subplot(2,2,4)
ax2.plot(lat, qflx_jja_zonal, linewidth=3.0, color = 'b', linestyle = '--', label='JJA')
ax2.plot(lat, qflx_djf_zonal, linewidth=3.0, color = 'r', linestyle = '--', label='DJF')
ax2.plot(lat, qflx_zonal, linewidth = 3.0, color = 'k', label = 'Annual')
ax2.legend(fontsize = 20)
#set ax2 format
ax2.set_title('d. Zonal average evaporation (1850-1980 AD)',fontweight = 'bold', fontsize = 20 )
ax2.set_xlabel('°N',fontsize = 16)
ax2.tick_params(labelsize=16) 
ax2.set_ylabel("cm/year",fontsize = 16)

#plot ax3 and ax4, seasonal evaporation
ax3 = fig.add_subplot(2,2,1, projection=ccrs.PlateCarree())
ax3.coastlines()
#plot ax3.controuf map
contf3 = ax3.contourf(lon,lat,qflx_jja_interval_ave, 
                      levels = np.linspace(lower_limitation,upper_limitation,51),
                      extend = 'both',
                      projection=ccrs.PlateCarree())
#set title for ax3
ax3.set_title('a. Average evaporation (JJA, 1850-1980 AD)', fontweight = 'bold', fontsize = 20)

#add colorbar
cb3 = fig.colorbar(contf3, ticks = np.linspace(lower_limitation,upper_limitation,11),  format = '%.0f',
                   orientation = 'horizontal',fraction=0.08, pad=0.1)
#set ax3.colorbar format
cb3.set_label('cm/year',  fontsize = 16)
cb3.ax.tick_params(labelsize=16)
#set ax3 label's and tick's format
ax3.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
ax3.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
ax3.tick_params(axis='both', labelsize=20)
ax3.xaxis.set_major_formatter(LongitudeFormatter())
ax3.yaxis.set_major_formatter(LatitudeFormatter())

ax4 = fig.add_subplot(2,2,2, projection=ccrs.PlateCarree())
ax4.coastlines()
#plot ax4.controuf map
contf4 = ax4.contourf(lon,lat,qflx_djf_interval_ave, 
                      levels = np.linspace(lower_limitation,upper_limitation,51),
                      extend = 'both',
                      projection=ccrs.PlateCarree())
#set title for ax4
ax4.set_title('b. Average evaporation (DJF, 1850-1980 AD)', fontweight = 'bold', fontsize = 20)

#add colorbar
cb4 = fig.colorbar(contf1, ticks = np.linspace(lower_limitation,upper_limitation,11),  format = '%.0f',
                   orientation = 'horizontal',fraction=0.08, pad=0.1)
#set ax4.colorbar format
cb4.set_label('cm/year',  fontsize = 16)
cb4.ax.tick_params(labelsize=16)
#set ax4 label's and tick's format
ax4.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
ax4.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
ax4.tick_params(axis='both', labelsize=20)
ax4.xaxis.set_major_formatter(LongitudeFormatter())
ax4.yaxis.set_major_formatter(LatitudeFormatter())

#####-------------------------------------------------------------------##########

fig.savefig('evap_annual_seasonal_zonal_1850_1980.png')