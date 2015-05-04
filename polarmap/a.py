import matplotlib.pyplot as plt
import polarmap

pmap = polarmap.PolarMap(-10, 30, 55, 65, "coast.npy", vlon=0)

#pmap.drawcoastlines()
pmap.fillcontinents(edgecolor='red')

parallels = [-55, 60, 65]
pmap.drawparallels(parallels)

plt.show()

