# -*- coding: utf-8 -*-

# -----------------------------------
# Bjørn Ådlandsvik <bjorn@imr.no>
# Institute of Marine Research
# -----------------------------------

import matplotlib.pyplot as plt
import polarmap

# Determine geographical extent
lon0, lon1 = -10, 30       # Longitude range
lat0, lat1 =  54, 72       # Latitude range

pmap = polarmap.PolarMap(lon0, lon1, lat0, lat1, 'coast.npy')
pmap.init_axis(color='LightBlue')

#pmap.drawcoastlines()
pmap.fillcontinents(facecolor='green', edgecolor='black')

pmap.drawparallels()
pmap.drawmeridians()


plt.show()
