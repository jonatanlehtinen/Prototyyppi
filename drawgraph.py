import matplotlib.pyplot as plt
import mysql.connector as mariadb
import pylab
import numpy as np
from mpl_toolkits.basemap import Basemap
import datetime


def getFromDataBase(time, code, lengthOfTime):

	#try:
	#Create connection to database
	mariadb_connection = mariadb.connect(user='root', password='pythontesti', database='Otaniemi')
	cursor = mariadb_connection.cursor()

	#Query for right data
	cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, latitude, longitude FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND postalcode LIKE %s AND radiotype='cell'", (time,lengthOfTime, time,code,))
	mariadb_connection.close()

	#return list including fetched data
	return list(cursor)
#except:
	print("Couldn't create database connection")
	#return []



def createMap():
	data = getFromDataBase(datetime.date(2016,6,13), "02150%", -30)
	#lat = [float(i[5]) for i in data]
	#lon = [float(i[6]) for i in data]
	map = Basemap(projection='merc', lon_0=24.82235, lat_0=60.17984, resolution = 'h', area_thresh = 0.001,llcrnrlat=60.165851, llcrnrlon=24.801312,urcrnrlat=60.193829, urcrnrlon=24.843388)
	map.drawcountries()
	map.fillcontinents(color='coral')
	map.drawmapboundary()
	for row in data:
		lat = [float(row[5])]
		lon = [float(row[6])]
		x,y = map(lon, lat)
		if row[3] < 10000:
			map.plot(x,y, 'bo', markersize = 1, color = "red")
		elif row[3] < 15000:
			map.plot(x,y, 'bo', markersize = 1, color = "yellow")
		else:
			map.plot(x,y, 'bo', markersize = 1, color = "green")
	#map.drawmeridians(np.arange(0, 360, 30))
	#map.drawparallels(np.arange(-90, 90, 30))
	 
	plt.show()


def drawGraph2(data):
	x = [1/24 * i[1] + 1 + i[0] for i in data]
	y1 = [i[2] for i in data]
	y2 = [i[3] for i in data]
	
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


