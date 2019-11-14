# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 17:24:31 2019

@author: Shihan Li
# plot seasonal precipitation and wind direction to show the monsoon system
"""
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
prect_jja_zonal = np.mean(prect_jja_interval_ave, axis = 1)
prect_djf_zonal = np.mean(prect_djf_interval_ave, axis = 1)
        
upper_limitation = 400

fig = plt.figure(figsize = (30,15))

#plot ax1, average jja precipitation in 1850-1980
ax1 = fig.add_subplot(221, projection=ccrs.PlateCarree())
ax1.coastlines(resolution='50m')
#plot ax1.controuf map
contf1 = ax1.contourf(lon,lat,prect_jja_interval_ave, levels = np.linspace(0,upper_limitation,51),
                      extend = 'max',
                      projection=ccrs.PlateCarree())
#set title for ax1
ax1.set_title('Average Precipitation (JJA, 1850-1980 AD)', fontweight = 'bold', fontsize = 20)
#plot the contour line
#levels = range(100,700,200)
#countour = ax1.contour(lon, lat, evap_ave, levels = levels, colors='r',linestyles = 'dashed')
#add colorbar
cb1 = fig.colorbar(contf1, ticks = np.linspace(0,upper_limitation,11),  format = '%.0f',
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
#plot ax2, average djf precipitation in 1850-1980

ax2 = fig.add_subplot(222, projection=ccrs.PlateCarree())
ax2.coastlines()
contf2 = ax2.contourf(lon,lat,prect_djf_interval_ave, levels = np.linspace(0,upper_limitation,51),
                      extend = 'max',
                      projection=ccrs.PlateCarree())
#set title for ax2
ax2.set_title('Average Precipitation (DJF, 1850-1980 AD)', fontweight = 'bold', fontsize = 20)
#plot the contour line
#levels = range(100,700,200)
#countour = ax1.contour(lon, lat, evap_ave, levels = levels, colors='r',linestyles = 'dashed')
#add colorbar
cb2 = fig.colorbar(contf2, ticks = np.linspace(0,upper_limitation,11),  format = '%.0f',
                   orientation = 'horizontal',fraction=0.08, pad=0.1)
#set ax2.colorbar format
cb2.set_label('cm/year',  fontsize = 16)
cb2.ax.tick_params(labelsize=16)
#set ax1 label's and tick's format
ax2.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
ax2.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
ax2.tick_params(axis='both', labelsize=20)
ax2.xaxis.set_major_formatter(LongitudeFormatter())
ax2.yaxis.set_major_formatter(LatitudeFormatter())
#ax1.set_extent([80, 140, -40, 40],crs=ccrs.PlateCarree())
#ax2.set_extent([80, 140, -40, 40], crs=ccrs.PlateCarree())

#read seasonal wind direction data
file_name_u_jja = ('trace.01-36.22000BP.cam2.U.22000BP_decavgJJA_400BCE.nc')
file_name_u_djf = ('trace.01-36.22000BP.cam2.U.22000BP_decavgDJF_400BCE.nc')
data_u_jja = readdata(file_name_u_jja)
data_u_djf = readdata(file_name_u_djf)
u_jja = data_u_jja.variables['U'][:,25,:,:]
u_djf = data_u_djf.variables['U'][:,25,:,:]
lon_uv = data_u_jja.variables['lon'][:]
lat_uv = data_u_jja.variables['lat'][:]
time = data_u_jja.variables['time'][:]
file_name_v_jja = ('trace.01-36.22000BP.cam2.V.22000BP_decavgJJA_400BCE.nc')
file_name_v_djf = ('trace.01-36.22000BP.cam2.V.22000BP_decavgDJF_400BCE.nc')
data_v_jja= readdata(file_name_v_jja)
data_v_djf= readdata(file_name_v_djf)
v_jja = data_v_jja.variables['V'][:,25,:,:]
v_djf = data_v_djf.variables['V'][:,25,:,:]


#define the time interval: 1850 - 1980 AD


u_jja_interval = u_jja[time_index[0][0]:time_index[0][-1]+1,:,:]
u_djf_interval = u_djf[time_index[0][0]:time_index[0][-1]+1,:,:]
v_jja_interval = v_jja[time_index[0][0]:time_index[0][-1]+1,:,:]
v_djf_interval = v_djf[time_index[0][0]:time_index[0][-1]+1,:,:]

#calculate the average in this time interval
u_jja_ave = np.empty([len(lat_uv),len(lon_uv)])
u_djf_ave = np.empty([len(lat_uv),len(lon_uv)])
v_jja_ave = np.empty([len(lat_uv),len(lon_uv)])
v_djf_ave = np.empty([len(lat_uv),len(lon_uv)])
for i in range(len(lat_uv)):
    for j in range(len(lon_uv)):
        u_jja_ave[i,j] = np.mean(u_jja_interval[:,i,j])
        u_djf_ave[i,j] = np.mean(u_djf_interval[:,i,j])
        v_jja_ave[i,j] = np.mean(u_jja_interval[:,i,j])
        v_djf_ave[i,j] = np.mean(u_djf_interval[:,i,j])
        
jja = ax1.quiver(lon_uv[::4],lat_uv[0:48:2],
              u_jja_ave[::2,::4],v_jja_ave[::2,::4])
              #scale_units = 'width',
              #width=0.007)
djf = ax2.quiver(lon_uv[::4],lat_uv[0:48:2],
              u_djf_ave[::2,::4],v_djf_ave[::2,::4])
              #scale_units = 'width',width=0.007
              

ax1.quiverkey(jja, 0.5, 0.89, 10, r'10m/s', labelpos='E', fontproperties={'size': 16},
                   coordinates='figure')
#ax2.quiverkey(djf, 0.83, 0.62, 10, r'10m/s', labelpos='E', fontproperties={'size': 16},
#                   coordinates='figure')

#plot ax3, JJA-DJF
ax3 = fig.add_subplot(223,projection = ccrs.PlateCarree())
ax3.coastlines()
contf3 = ax3.contourf(lon,lat,prect_jja_interval_ave - prect_djf_interval_ave,
                      levels = np.linspace(-300,300,61),
                      extend = 'both',
                      projection = ccrs.PlateCarree())
ax3.set_title('Seasonal precipitation difference (JJA-DJF, 1850-1980 AD)', fontweight = 'bold',
              fontsize = 20)
#contour = ax3.contour(lon,lat,prect_jja_interval_ave - prect_djf_interval_ave, levels=0,
#                      colors = 'r')
#ax3.clabel(contour, contour.levels, fmt = '%.0f', fontsize = 20)
cb3 = fig.colorbar(contf3, #ticks = np.linspace(0,upper_limitation,11),  
                   format = '%.0f',
                   orientation = 'horizontal',fraction=0.08, pad=0.1)
cb3.set_label('cm/year',  fontsize = 16)
cb3.ax.tick_params(labelsize=16)
ax3.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
ax3.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
ax3.tick_params(axis='both', labelsize=20)
ax3.xaxis.set_major_formatter(LongitudeFormatter())
ax3.yaxis.set_major_formatter(LatitudeFormatter())

ax4 = fig.add_subplot(224)
ax4.plot(lat, prect_jja_zonal, linewidth=3.0, color = 'b', label='JJA')
ax4.plot(lat, prect_djf_zonal, linewidth=3.0, color = 'r', linestyle = '--', label='DJF')
ax4.legend(fontsize = 20)
#set ax4 format
ax4.set_title('Zonal Average Precipitation (1850-1980 AD)',fontweight = 'bold', fontsize = 20 )
ax4.set_xlabel('°N',fontsize = 16)
ax4.tick_params(labelsize=16) 
ax4.set_ylabel("cm/year",fontsize = 16)

fig.savefig("seasonal_prect_ave_plus_wind_field_1850_1980.png")
#ax1.set_extent([-180, 180, -40, 40],crs=ccrs.PlateCarree())
#ax2.set_extent([-180, 180, -40, 40], crs=ccrs.PlateCarree())