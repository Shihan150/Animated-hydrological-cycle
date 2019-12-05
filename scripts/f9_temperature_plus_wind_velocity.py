
"""
Created on Fri Oct 25 11:19:28 2019

@author: Shihan Li
plot the surface temperature and surface wind velocity vector for 1850-1980 AD
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
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

file_name1 = ('trace.01-36.22000BP.cam2.TS.22000BP_decavg_400BCE.nc')
data_q = readdata(file_name1)
lon = data_q.variables['lon'][:]
lat = data_q.variables['lat'][:]
time = data_q.variables['time'][:]
q = data_q.variables['TS'][:,:,:] -273.15


lon = np.append(lon, 360)
q = np.dstack((q,q[:,:,0])) 

    
#process the ocean fraction data
file_name_ocnfrac = ('trace.01-36.22000BP.cam2.OCNFRAC.22000BP_decavg_400BCE.nc')
data_ocnfrac = readdata(file_name_ocnfrac)
ocnfrac = data_ocnfrac.variables['OCNFRAC'][:] 
ocnfrac = np.dstack((ocnfrac, ocnfrac[:,:,0])) 

#define the time interval: 1850 - 1980 AD
time_index = np.where((time>=-0.1))
time_interval = time[time_index]

q_interval = q[time_index[0][0]:time_index[0][-1]+1,:,:]
ocnfrac_interval = ocnfrac[time_index[0][0]:time_index[0][-1]+1,:,:]


#calculate the average in this time interval
q_ave = np.empty([len(lat),len(lon)])
ocnfrac_ave = np.empty([len(lat),len(lon)])
for i in range(len(lat)):
    for j in range(len(lon)):
        q_ave[i,j] = np.mean(q_interval[:,i,j])
        ocnfrac_ave[i,j] = np.mean(ocnfrac_interval[:,i,j])
        
        
ocnfrac_ave[ocnfrac_ave!= 0] = 1
ocnfrac_ave[ocnfrac_ave==0] = None

q_ave *= ocnfrac_ave



#define the upper limitation for contourf plot
upper_limitation = 30
#lower_limitation = np.min(q_ave)




#read U,V data
file_name_u = ('trace.01-36.22000BP.cam2.U.22000BP_decavg_400BCE.nc')
data_u = readdata(file_name_u)
u = data_u.variables['U'][:,25,:,:]
lon1 = data_u.variables['lon'][:]
lat1 = data_u.variables['lat'][:]
time = data_u.variables['time'][:]
file_name_v = ('trace.01-36.22000BP.cam2.V.22000BP_decavg_400BCE.nc')
data_v= readdata(file_name_v)
v = data_v.variables['V'][:,25,:,:]


#define the time interval: 1850 - 1980 AD
time_index = np.where((time>=-0.1))
time_interval = time[time_index]

u_interval = u[time_index[0][0]:time_index[0][-1]+1,:,:]
v_interval = v[time_index[0][0]:time_index[0][-1]+1,:,:]

#calculate the average in this time interval
u_ave = np.empty([len(lat),len(lon1)])
v_ave = np.empty([len(lat),len(lon1)])
for i in range(len(lat)):
    for j in range(len(lon1)):
        u_ave[i,j] = np.mean(u_interval[:,i,j])
        v_ave[i,j] = np.mean(v_interval[:,i,j])

fig = plt.figure(figsize = (20,12))
ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
ax.coastlines(resolution='110m')
#plot controuf map
contf = ax.contourf(lon,lat,q_ave, levels = np.linspace(-10,upper_limitation,20),
                    extend = 'max',
                      projection=ccrs.PlateCarree())
cont = ax.contour(lon,lat,q_ave, levels = (20,28), linewidths =2, colors = ['black','red'],
                  projection=ccrs.PlateCarree())
ax.clabel(cont, cont.levels, fmt = '%.0f', fontsize = 20)
#set title for ax1
ax.set_title('Average sea surface temperature and wind field (1850-1980 AD)', 
             fontweight = 'bold', fontsize = 20,pad=20)
#add colorbar
cb = fig.colorbar(contf, ticks = np.linspace(-10, upper_limitation, 10),  format = '%.0f',
                   orientation = 'horizontal',fraction=0.08, pad=0.1)
#set ax1.colorbar format
cb.set_label('Surface Temperature (°C)',  fontsize = 16)
cb.ax.tick_params(labelsize=16)
#set ax1 label's and tick's format
ax.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
ax.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
ax.tick_params(axis='both', labelsize=20)
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())

wind_field = ax.quiver(lon1[::4],lat1[0:48:2],
              u_ave[::2,::4],v_ave[::2,::4])
ax.quiverkey(wind_field, 0.85, 0.9, 10, r'10m/s', labelpos='E', fontproperties={'size': 16} ,
                   coordinates='figure')


fig.savefig('surface_layer_temperature_wind_field_1850_1980.png')

