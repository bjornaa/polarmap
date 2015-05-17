# -*- coding: utf-8 -*-

# Quick and dirty plot of topography

import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

topo_file = 'topo.nc'

# Load the topography
with Dataset(topo_file) as fid:
    lon = fid.variables['lon'][:]
    lat = fid.variables['lat'][:]
    topo = fid.variables['topo'][:,:]

# Plot the topography
plt.contourf(lon, lat, topo)
plt.colorbar()
plt.show()
