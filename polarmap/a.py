import matplotlib.pyplot as plt
import polarmap

pmap = polarmap.PolarMap(-10, 30, 55, 65, "coast.npy", vlon=-10)


pmap.init_axis()
#pmap.drawcoastlines()
pmap.fillcontinents(edgecolor='red')

plt.show()

