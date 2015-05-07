# -*- coding: utf-8 -*-

"""Quick and dirty plot of a coast line

Usage: python plotcoast.py coast_file

"""

# -----------------------------------
# Bjørn Ådlandsvik <bjorn@imr.no>
# Institute of Marine Research
# -----------------------------------

import sys
import numpy as np
import matplotlib.pyplot as plt

# Get the name of the coast file from the command line
try:
    coastfile = sys.argv[1]
except IndexError:
    print("Usage: python plotcoast.py coastfile")
    sys.exit(-1)

# Load the coast line
try:
    polys = np.load(coastfile)
except IOError:
    print("Not a valid npy-file: " + coastfile)
    sys.exit(-2)

# Make the land polygons green
for p in polys:
    plt.fill(p[0], p[1], color='green')

plt.show()
