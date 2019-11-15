# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 10:28:11 2019

@author: Shihan Li
plot the streamfunction of ocean current in Atlantic and Pacific
"""
#import packages
import numpy as np
import matplotlib.pyplot as plt


#readdata function
from netCDF4 import Dataset
def readdata(file_name):
    file_path_re = r'D:\LifeInBremen\MODULES\Project\data\ocean'
    b = '/'
    file_path = file_path_re + b + file_name
    file_obj = Dataset(file_path)
    print(file_obj.variables.keys())
    return file_obj

#read the data
file_name = 'trace.01-36.22000BP.pop.MOC.22000BP_decavg_400BCE.nc'
data_moc = readdata(file_name)
moc = data_moc.variables['MOC'][:,:,0,:,:]
lat = data_moc.variables['lat_aux_grid'][:]
#convert cm - km
moc_z = data_moc.variables['moc_z'][:]/100000
time = data_moc.variables['time'][:]

time_index = np.where((time>=-0.1))
time_interval = time[time_index]

#transport_regions[0]:Atl, transport_regions[0]:Pac
moc_atl_interval = moc[time_index[0][0]:time_index[0][-1]+1,1,:,:]
moc_pac_interval = moc[time_index[0][0]:time_index[0][-1]+1,0,:,:]

#calculate the average in this time interval
moc_atl_ave = np.empty([len(moc_z),len(lat)])
moc_pac_ave = np.empty([len(moc_z),len(lat)])
for i in range(len(moc_z)):
    for j in range(len(lat)):
        moc_atl_ave[i,j] = np.mean(moc_atl_interval[:,i,j])
        moc_pac_ave[i,j] = np.mean(moc_pac_interval[:,i,j])
        
####---------------------plot the figure---------------------#####

fig = plt.figure(figsize = (18,5))

ax1 = fig.add_subplot(1,2,1)
contf1 = ax1.contourf(lat,moc_z, moc_atl_ave,extend = 'both' )
cont1 = ax1.contour(lat, moc_z, moc_atl_ave)
ax1.clabel(cont1, cont1.levels,fmt = '%.0f', colors = 'black',fontsize =12)
cb1 = fig.colorbar(contf1,  format = '%.0f',
                   orientation = 'horizontal',fraction=0.08, pad=0.15)
cb1.set_label('Sv',  fontsize = 16)
cb1.ax.tick_params(labelsize=16)
ax1.set_xlabel('°N',fontsize = 16)
ax1.tick_params(labelsize=16) 
ax1.set_ylabel("Depth (km)",fontsize = 16)
ax1.axes.set_ylim([-0.5,5])
ax1.axes.set_xlim([-80,95])
#hide the spines of ax1
ax1.spines['top'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
plt.gca().invert_yaxis()
#ax.clabel(cont, cont.levels, fmt = '%.0f', #fontsize = 15,
#         colors = 'b')

ax2 = fig.add_subplot(1,2,2)
contf2 = ax2.contourf(lat, moc_z, moc_pac_ave,levels = np.linspace(-10,30,21),extend = 'both')
cont2 = ax2.contour(lat, moc_z, moc_pac_ave, levels = np.linspace(-10,30,6), linewidth = '2')
ax2.clabel(cont2, cont2.levels,fmt = '%.0f', colors = 'black', fontsize = 12)
cb2 = fig.colorbar(contf2,  format = '%.0f',
                   orientation = 'horizontal',fraction=0.08, pad=0.15)
cb2.set_label('Sv',  fontsize = 16)
cb2.ax.tick_params(labelsize=16)

ax2.set_xlabel('°N',fontsize = 16)
ax2.tick_params(labelsize=16) 
ax2.set_ylabel("Depth (km)",fontsize = 16)
ax2.axes.set_ylim([-0.5,5])
ax2.axes.set_xlim([-80,95])
#hide the spines of ax2
ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
plt.gca().invert_yaxis()
fig.savefig("moc_1850_1980.jpg")