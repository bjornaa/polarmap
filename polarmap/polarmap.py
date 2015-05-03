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
import roppy

# Radian factor
rad = np.pi / 180.0

class PolarMap(object):
    """Polar stereographic map from South pole onto equator"""
    def __init__(self, lon0, lon1, lat0, lat1,
                 coastfile, vlon=None):
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

        # Use nice_levels to find tick values for lon and lat
        self.lon_ticks = roppy.nice_levels(self.lon0, self.lon1)
        self.lat_ticks = roppy.nice_levels(self.lat0, self.lat1)

    def __call__(self, lon, lat):
        lon = np.asarray(lon)
        lat = np.asarray(lat)
        m =  np.tan((45.0-0.5*lat)*rad)    # Stereographic
        x =  m*np.sin((lon-self.vlon)*rad)
        y = -m*np.cos((lon-self.vlon)*rad)
        return x, y 

    def init_axis(self):
        # Make white background plot area and store as clipping path
        self.clip_path, = plt.fill(self.xbry, self.ybry,
                                   facecolor='white', zorder=-2)
        # Plot a black foreground frame for the plot area
        plt.plot(self.xbry, self.ybry, color='black')

        # Make a thight of correct aspect ration and save it
        plt.axis('image')
        self.axis_limits = plt.axis()

        # Make tickmarks
        self._make_lon_ticks()
        self._make_lat_ticks()

        # Hide the standard matplotlib axes
        a = plt.gca()
        a.set_axis_bgcolor(plt.gcf().get_facecolor())
        a.set_axis_off()

        plt.axis(self.axis_limits)
        plt.axis('image')

    def _make_lon_ticks(self):
        lat0 = self.lat0
        ticklen = 0.002
        labelsep = 0.003
        for lon in self.lon_ticks:
            angle = lon-self.vlon
            cosa = np.cos(angle*rad)
            sina = np.sin(angle*rad)
            x0, y0 = self(lon, lat0)
            x1 = x0 + ticklen*sina
            y1 = y0 - ticklen*cosa
            x2 = x0 + labelsep*sina
            y2 = y0 - labelsep*cosa
            
            #x, y = self([lon, lon], [lat0, lat0-ticklen/60.0])
            plt.plot([x0, x1], [y0, y1], 'k', clip_on=False)
            #x, y = self(lon, lat0-lon_labelsep/60.0)
            plt.text(x2, y2, str(lon), 
                     rotation = angle,
                     rotation_mode = 'anchor',
                     horizontalalignment='center',
                     verticalalignment='top')
        
    def _make_lat_ticks(self):
        # Left latitude ticks
        lon0 = self.lon0
        label_angle = 0.5*(self.lon0 - self.lon1)
        ticklen = 0.002
        labelsep = 0.003
        cosa = np.cos(label_angle*rad)
        sina = np.sin(label_angle*rad)
        
        for lat in self.lat_ticks:
            x0, y0 = self(lon0, lat)
            x1 = x0 - ticklen * cosa
            y1 = y0 - ticklen * sina
            x2 = x0 - labelsep * cosa
            y2 = y0 - labelsep * sina
            plt.plot([x0,x1], [y0,y1], 'k', clip_on=False)
            t = plt.text(x2, y2, str(lat),
                     rotation = label_angle,
                     rotation_mode = 'anchor',
                     horizontalalignment='right',
                     verticalalignment='center')

    def drawparallels(self):
        lon = np.linspace(self.lon0, self.lon1, 100)
        for lat in self.lat_ticks:
            x, y = self(lon, lat+np.zeros_like(lon))
            plt.plot(x, y, color='black', linestyle=':')
                
    def drawmeridians(self):
        for lon in self.lon_ticks:
            x, y = self([lon, lon], [self.lat0, self.lat1])
            plt.plot(x, y, color='black', linestyle=':')

    def drawcoastlines(self, *args, **kwargs):
        myplot = partial(plt.plot, color='black')
        for p in self.coast_polygons:
            x, y = self(p[0], p[1])
            h = myplot(x, y, *args, **kwargs)
            h[0].set_clip_path(self.clip_path)

    def fillcontinents(self, *args, **kwargs):
        myfill = partial(plt.fill, color='0.8')
        for p in self.coast_polygons:
            x, y = self(p[0], p[1])
            h = myfill(x, y, *args, **kwargs)
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

                



