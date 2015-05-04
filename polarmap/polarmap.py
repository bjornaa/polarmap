# -*- coding: utf-8 -*-

"""A class for Polar Stereographic maps with matplotlib"""

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

class PolarMap(object):
    """Polar stereographic map from South pole onto equator"""

    def __init__(self, lon0, lon1, lat0, lat1,
                 coastfile, vlon=None, facecolor='white'):
        self.lon0 = lon0
        self.lon1 = lon1
        self.lat0 = lat0
        self.lat1 = lat1
        #self.coastfile = coastfile

        if vlon is None:
            self.vlon = 0.5*(lon0 + lon1)
        else:
            self.vlon = vlon

        # Map boundary
        lon_bry = np.concatenate((np.linspace(lon0, lon1, 50),
                                  np.linspace(lon1, lon0, 50),
                                  [lon0]))
        lat_bry = np.concatenate((lat0+np.zeros((50,)),
                                  lat1+np.zeros((50,)),
                                  [lat0]))
        self.xbry, self.ybry = self(lon_bry, lat_bry)

        # Coast line
        self.coast_polygons = np.load(coastfile)

        # Initiate maplotlib axis
        # ------------------------

        # Make white background plot area and store as clipping path
        self.clip_path, = plt.fill(self.xbry, self.ybry,
                                   facecolor=facecolor, zorder=-2)
        # Plot a black foreground frame for the plot area
        plt.plot(self.xbry, self.ybry, color='black', lw=2)

        # Make a thight of correct aspect ration and save it
        plt.axis('image')
        self.axis_limits = plt.axis()

        # Hide the standard matplotlib axes
        a = plt.gca()
        a.set_axis_bgcolor(plt.gcf().get_facecolor())
        a.set_axis_off()

        plt.axis(self.axis_limits)
        plt.axis('image')

    def __call__(self, lon, lat):
        """Call the instance to project from lon/lat"""
        
        lon = np.asarray(lon)
        lat = np.asarray(lat)
        m =  np.tan((45.0-0.5*lat)*rad)    # Stereographic
        x =  m*np.sin((lon-self.vlon)*rad)
        y = -m*np.cos((lon-self.vlon)*rad)
        return x, y

    def drawparallels(self, parallels, **kwargs):
        """Draw and label parallels"""
        
        labelsep = 0.003
        myplot = partial(plt.plot, color='black', linestyle=':')
        lon = np.linspace(self.lon0, self.lon1, 100)

        label_angle = self.lon0 - self.vlon
        cosa = np.cos(label_angle*rad)
        sina = np.sin(label_angle*rad)

        for lat in parallels:
            x, y = self(lon, lat+np.zeros_like(lon))
            myplot(x, y, **kwargs)
            # Labels
            x0, y0 = self(self.lon0, lat)
            x1 = x0 - labelsep * cosa
            y1 = y0 - labelsep * sina
            t = plt.text(x1, y1, str(lat),
                     rotation = label_angle,
                     rotation_mode = 'anchor',
                     horizontalalignment='right',
                     verticalalignment='center')

    def drawmeridians(self, meridians, **kwargs):
        """Draw and label meridians"""
        myplot = partial(plt.plot, color='black', linestyle=':')
        labelsep = 0.003
        for lon in meridians:
            # Plot meridians
            x, y = self([lon, lon], [self.lat0, self.lat1])
            myplot(x, y, **kwargs)

            # Labels
            angle = lon-self.vlon
            cosa = np.cos(angle*rad)
            sina = np.sin(angle*rad)
            x0, y0 = self(lon, self.lat0)
            x1 = x0 + labelsep*sina
            y1 = y0 - labelsep*cosa
            plt.text(x1, y1, str(lon),
                     rotation = angle,
                     rotation_mode = 'anchor',
                     horizontalalignment='center',
                     verticalalignment='top')

    def drawcoastlines(self, **kwargs):
        """Draw the coast line"""
        
        myplot = partial(plt.plot, color='black')
        for p in self.coast_polygons:
            x, y = self(p[0], p[1])
            h = myplot(x, y, *args, **kwargs)
            h[0].set_clip_path(self.clip_path)

    def fillcontinents(self, **kwargs):
        """Fill land"""
        
        myfill = partial(plt.fill, color='0.8')
        for p in self.coast_polygons:
            x, y = self(p[0], p[1])
            h = myfill(x, y, **kwargs)
            h[0].set_clip_path(self.clip_path)

    # Wrap some plotting methods

    def contourf(self, lon, lat, data, *args, **kwargs):
        x, y = self(lon, lat)
        h = plt.contourf(x, y, data, *args, **kwargs)
        for q in h.collections:
            q.set_clip_path(self.clip_path)
        return h

    def contour(self, lon, lat, data, *args, **kwargs):
        x, y = self(lon, lat)
        h = plt.contour(x, y, data, *args, **kwargs)
        for q in h.collections:
            q.set_clip_path(self.clip_path)
        return h

    def plot(self, lon, lat, *args, **kwargs):
        x, y = self(lon, lat)
        h = plt.plot(x, y, *args, **kwargs)
        h[0].set_clip_path(self.clip_path)

    def fill(self, lon, lat, *args, **kwargs):
        x, y = self(lon, lat)
        h = plt.fill(x, y, *args, **kwargs)
        h[0].set_clip_path(self.clip_path)
