# -*- coding: utf-8 -*-

# -----------------------------------
# Bjørn Ådlandsvik <bjorn@imr.no>
# Institute of Marine Research
# -----------------------------------

import matplotlib.pyplot as plt
import polarmap

# Define geographical extent
lon0, lon1 = -10, 30       # Longitude range
lat0, lat1 =  54, 72       # Latitude range

pmap = polarmap.PolarMap(lon0, lon1, lat0, lat1, 'coast.npy',
                         facecolor='LightBlue')

pmap.fillcontinents(facecolor='green', edgecolor='black')

pmap.drawparallels([55, 60, 65, 70])
pmap.drawmeridians([-10, 0, 10, 20, 30])

plt.show()
