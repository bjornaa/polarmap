# -*- coding: utf-8 -*-

# Plot bathymetry on a polar map

# -----------------------------------
# Bjørn Ådlandsvik <bjorn@imr.no>
# Institute of Marine Research
# -----------------------------------

# ---------
# Imports
# ---------

import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mercator import MercatorMap

# ---------------
# User settings
# ---------------

# Define geographical extent
lon0, lon1 = -10, 30       # Longitude range
lat0, lat1 =  54, 72       # Latitude range

lons = range(-10, 31, 10)
lats = range(55, 71, 5)

# Topography file
topo_file = 'topo.nc'

# Select vertical levels
levels = [1, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]

# --- End user settings --------

# Level treatment
loglevels = [np.log10(v) for v in levels]
level_labels = ['0'] + [str(v) for v in levels[1:]]  # Use '0' instead of '1'

# Load the topography
with Dataset(topo_file) as fid:
    lon = fid.variables['lon'][:]
    lat = fid.variables['lat'][:]
    topo = fid.variables['topo'][:, :]
llon, llat = np.meshgrid(lon, lat)

# Depth is positive and only defined at sea
topo = np.where(topo >= 0, np.nan, -topo)

# Define the PolarMap instance
pmap = MercatorMap(lon0, lon1, lat0, lat1, 'coast.npy')

# Contour the bathymetry
pmap.contourf(llon, llat, np.log10(topo),
              cmap=plt.get_cmap('Blues'),
              levels=loglevels,
              extend='max')

# Colorbar
plt.colorbar(ticks=loglevels,
             format=plt.FixedFormatter(level_labels),
             extend='max',
             shrink=0.8)

# Put a yellow colour on land with a black coast line
pmap.fillcontinents(facecolor=(0.8, 0.8, 0.2), edgecolor='black')

# Draw graticule
pmap.drawparallels(lats)
pmap.drawmeridians(lons)

plt.show()
