#!/usr/bin/env python
# -*- coding: utf-8 -*-


# --------------------------------------
# Bjørn Ådlandsvik   <bjorn@imr.no>
# Institute of Marine Research
# 2011-01-02
# --------------------------------------

# ---------------
# Imports
# ---------------

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import sys
import roppy
from roppy.mpl_util import  LevelColormap
from polarmap import PolarMap

# ---------------
# User settings
# ---------------

# ROMS data file
roms_file = '../data/norkyst_800m_grid_Lus.nc'

# Coast file
coast_file = '../data/coast.dat'

# Geographical extent
lon0, lon1 = -1, 35
lat0, lat1 = 56, 74
#lon0, lon1 = -12, 12
#lat0, lat1 =  49, 65
#lon0, lon1 = -70, 120
#lat0, lat1 = 40, 90


# Isolevels for depth
Levels = (0,50,100,200,300,400,500,1000,2000,3000)

# ------------------
# Read data
# ------------------

f = Dataset(roms_file)
grd = roppy.SGrid(f)
#f.close()

lon_coast, lat_coast = np.loadtxt(coast_file, unpack=True)

# ------------------
# Data handling
# ------------------

# Define polar stereographic projection
pmap = PolarMap(lon0, lon1, lat0, lat1)

# Mask out the Baltic
H = grd.h
H[0:100, 600:2000] = np.nan




# Plot
# ------------

plt.rcParams['savefig.bbox'] = "tight"

fig = plt.figure(figsize=(20, 20))


# Make polar axis
pmap.init_axis()
#ax = plt.gca()

# Reverse and spread out the default colour map
cmap = LevelColormap(Levels, reverse=True)

# Plot the bottom topography
pmap.contourf(grd.lon_rho, grd.lat_rho, H, levels=Levels,
             cmap=cmap, extend='max')
plt.colorbar(drawedges=True, shrink=0.4, pad=-0.33)
# Add black contour lines
pmap.contour(grd.lon_rho, grd.lat_rho, grd.h, levels=Levels, colors='black')

# Plot land
pmap.fill(lon_coast, lat_coast, facecolor='0.8')

# Draw graticule
pmap.drawparallels()
pmap.drawmeridians()

# Display the graphics
plt.savefig("domain.png", dpi=200)
#plt.show()



