Polarmap
========

.. figure:: scandinavia.png
   :scale: 30%

   An non-rectangular polar stereographic map of Scandinavia


The standard map plotting package for python+matplotlib
is basemap. This is a flexible package with a lot of map
projections. However, it seems like basemap can not produce
non-rectangular regional polar stereographic maps like Matlab's
m-map or the Generic Mapping Tools (GMT).

This map type is useful for relatively high latitudes where
the Mercator projection is highly distorted.

Polarmap is a simple package providing this kind of functionality
for python+matplotlib. This is a poor man's solution. Better options
would be to include this kind of map in basemap or implement it using
matplotlib projection functionality. Both these approaches are to
complicated for me.

Example use
-----------

First a coast line is needed. The makecoast script uses basemap for
this task and saves it to a npy file. This can be reused, using it
efficient for multiple plots on the same map domain.

from polarmap import PolarMap


