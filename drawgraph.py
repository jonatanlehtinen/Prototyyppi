import matplotlib.pyplot as plt
import pylab
import numpy as np
from mpl_toolkits.basemap import Basemap




def createMap():
	map = Basemap(projection='merc', lon_0=65, lat_0=27,
	resolution = 'h', area_thresh = 0.1,
	llcrnrlat=59.85, llcrnrlon=19.49,
	urcrnrlat=70.35, urcrnrlon=31.48)
	 
	map.drawcountries()
	map.fillcontinents(color='coral')
	map.drawmapboundary()
	lat = 60.45
	lon = 22.27
	#for row in data:
		
	x,y = map(lon, lat)
	map.plot(x,y, 'bo', markersize = 4)
	#map.drawmeridians(np.arange(0, 360, 30))
	#map.drawparallels(np.arange(-90, 90, 30))
	 
	plt.show()


def drawGraph2(data):
	x = [1/24 * i[1] + 1 + i[0] for i in data]
	y1 = [i[2] for i in data]
	y2 = [i[3] for i in data]
	print(x)
	
	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	ax1.plot(x, y1, color="red", marker = "o")
	ax1.plot(x, y2, color = "blue")
	
	ax1.set_title("Otaniemen data 2016, viikottaiset keskiarvot tunnettain")
	plt.xlabel("Day")
	plt.ylabel("Speed(kbps)")
	plt.show()
	



def drawGraph(data):

	print(data)
	x1 = [i[0] for i in data]
	y1 = [i[1] for i in data]
	y2 = [i[2] for i in data]

	maxY = max(y1+y2)
	minY = min(y1+y2)
	minX = min(x1)

	y3 = [i[3] for i in data]
	
	fig2 = plt.figure()
	ax1 = fig2.add_subplot(111)
	ax1.plot(x1, y3)	
	
	fig1 = plt.figure()
	ax = fig1.add_subplot(111)
	ax.plot(x1,y1, color = "red", marker = "o")
	ax.plot(x1,y2, color = "blue", marker = "o")
	ax.grid(True)
	plt.ylim(max(0,minY - 7000),maxY + 7000)
	plt.xlim(0, 23)
	ax.set_title("Otaniemen data 2016")
	ax.text(int(minX+1), int(maxY+4000), "Red plot: download", fontsize=13)
	ax.text(int(minX+1), int(maxY), "Blue plot: upload", fontsize=13)
	plt.xlabel("Hour")
	plt.ylabel("Speed(kbps)")
	plt.show()

'''from pylab import figure, axes, pie, title, show
import pylab

# Make a square figure and axes
figure(1, figsize=(6, 6))
ax = axes([0.1, 0.1, 0.8, 0.8])

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
fracs = [15, 30, 45, 10]

explode = (0, 0.05, 0, 0)
pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
title('Raining Hogs and Dogs', bbox={'facecolor': '0.8', 'pad': 5})

pylab.savefig('foo.png')
'''


