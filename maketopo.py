# -*- coding: utf-8 -*-

# Extract topography from etopo5
# using OPEeNDAP
#

# ---------------------------------
# Bjørn Ådlandsvik <bjorn@imr.no>
# Institute of Marine Research
# ---------------------------------

from __future__ import division

import numpy as np
from netCDF4 import Dataset

# Determine geographical extent
lon0, lon1 = -12, 50       # Longitude range
lat0, lat1 =  50, 80       # Latitude range

# URL of OPeNDAP server
url = 'http://ferret.pmel.noaa.gov/thredds/dodsC/data/PMEL/etopo5.nc'

# Read in etopo5 topography/bathymetry.
etopo5 = Dataset(url)

step = 5 / 60  # 5 minutes

# Lats from -90 to +90 (including) in 5 degree steps
j0 = int(round((lat0 + 90) / step))
j1 = int(round((lat1 + 90) / step))
lat = etopo5.variables['ETOPO05_Y'][j0:j1+1]

# Lons from 0 to 360 in 5 degree steps
# We have -180 <= lon0 < lon1 < 180
i0 = int(round((lon0 % 360) / step))
i1 = int(round((lon1 % 360) / step))

if lon0*lon1 >= 0:
    # Region does not cross zero meridian
    lon = etopo5.variables['ETOPO05_X'][i0:i1+1]
    west = (lon > 180)  # Western hemisphere
    lon[west] -= 360
    topo = etopo5.variables['ROSE'][j0:j1+1, i0:i1+1]
    # Undo masking of values = -1.0 at the coast
    topo = topo.data

else:
    # Read western and eastern hemisphere separately
    lon0 = etopo5.variables['ETOPO05_X'][i0:-1] - 360
    lon1 = etopo5.variables['ETOPO05_X'][0:i1+1]
    topo0 = etopo5.variables['ROSE'][j0:j1+1, i0:-1]
    topo1 = etopo5.variables['ROSE'][j0:j1+1, 0:i1+1]
    lon = np.concatenate((lon0, lon1))
    topo = np.concatenate((topo0, topo1), axis=1)

with Dataset('topo.nc', mode='w', format='NETCDF3_CLASSIC') as f:
    # Dimensions
    f.createDimension('lon', len(lon))
    f.createDimension('lat', len(lat))
    # Variables
    v = f.createVariable('lon', 'f', ('lon',))
    v.standard_name = 'longitude'
    v.units = "degree_east"
    v = f.createVariable('lat', 'f', ('lat',))
    v.standard_name = 'latitude'
    v.units = "degree_north"
    v = f.createVariable('topo', 'f', ('lat', 'lon'))
    v.long_name = 'topography'
    v.standard_name = 'altitude'
    v.units = "m"
    # Data
    f.variables['lon'][:] = lon
    f.variables['lat'][:] = lat
    f.variables['topo'][:, :] = topo
