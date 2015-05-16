# -*- coding: utf-8 -*-

"""A class for Mercator maps with matplotlib"""

# --------------------------------------
# Bjørn Ådlandsvik   <bjorn@imr.no>
# Institute of Marine Research
# --------------------------------------

# TODO:
# Better documentation
# Control over tickmark lengths

# ---------------
# Imports
# ---------------

from functools import partial

import numpy as np
import matplotlib.pyplot as plt

# Radian factor
rad = np.pi / 180.0
deg = 180.0 / np.pi

def merc(lat):
    return deg * np.log(np.tan((45 + 0.5*lat)*rad))
    


class MercatorMap(object):
    """Mercator map"""

    def __init__(self, lon0, lon1, lat0, lat1,
                 coastfile, facecolor='white'):
        self.lon0 = lon0
        self.lon1 = lon1
        self.lat0 = lat0
        self.lat1 = lat1
        
        # Coast line
        self.coast_polygons = np.load(coastfile)

        # Initiate maplotlib axis
        # ------------------------

        # Set axis limits
        plt.axis([lon0, lon1, merc(lat0), merc(lat1)])

        # Background colour
        plt.gca().set_axis_bgcolor(facecolor)

        # Turn off ordinary ticks and labels
        plt.xticks([])
        plt.yticks([])
        
    def __call__(self, lon, lat):
        """Call the instance to project from lon/lat"""

        lon = np.asarray(lon)
        lat = np.asarray(lat)
        x = lon
        y = merc(lat)
        return x, y

    def drawparallels(self, parallels, **kwargs):
        """Draw and label parallels"""
        myplot = partial(plt.plot, color='black', linestyle=':')
        for lat in parallels:
            x, y = self([self.lon0, self.lon1], [lat, lat])
            myplot(x, y, **kwargs)
        # Labels
        plt.yticks([merc(lat) for lat in parallels],  parallels)

    def drawmeridians(self, meridians, **kwargs):
        """Draw and label meridians"""
        myplot = partial(plt.plot, color='black', linestyle=':')
        for lon in meridians:
            # Plot meridians
            x, y = self([lon, lon], [self.lat0, self.lat1])
            myplot(x, y, **kwargs)
        # Labels
        plt.xticks(meridians)
            

    def drawcoastlines(self, **kwargs):
        """Draw the coast line"""

        myplot = partial(plt.plot, color='black')
        for p in self.coast_polygons:
            x, y = self(p[0], p[1])
            myplot(x, y, *args, **kwargs)

    def fillcontinents(self, **kwargs):
        """Fill land"""

        myfill = partial(plt.fill, facecolor='0.8', edgecolor='black')
        for p in self.coast_polygons:
            x, y = self(p[0], p[1])
            myfill(x, y, **kwargs)

    # Wrap some plotting methods

    def contourf(self, lon, lat, data, *args, **kwargs):
        x, y = self(lon, lat)
        h = plt.contourf(x, y, data, *args, **kwargs)
        #for q in h.collections:
        #    q.set_clip_path(self.clip_path)
        return h

    def contour(self, lon, lat, data, *args, **kwargs):
        x, y = self(lon, lat)
        h = plt.contour(x, y, data, *args, **kwargs)
        #for q in h.collections:
        #    q.set_clip_path(self.clip_path)
        return h

    def plot(self, lon, lat, *args, **kwargs):
        x, y = self(lon, lat)
        h = plt.plot(x, y, *args, **kwargs)
        #h[0].set_clip_path(self.clip_path)

    def fill(self, lon, lat, *args, **kwargs):
        x, y = self(lon, lat)
        h = plt.fill(x, y, *args, **kwargs)
        #h[0].set_clip_path(self.clip_path)
