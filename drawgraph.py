import matplotlib.pyplot as plt
import pylab
import numpy as np


def drawGraphLongTime(data,location):
	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	ax1.set_title(location)

	ax1.plot([i[0] for i in data[0]], [i[1] for i in data[0]], color = "red")

	fig1.autofmt_xdate()
	
	plt.show()

def drawGraphWeekCross(data, key, resolution):
	x = [1/24 * i[1] + 1 + i[0] for i in data]
	y1 = [i[2] for i in data]
	y2 = [i[3] for i in data]

	averageY1 = sum(y1) / len(y1)
	averageY2 = sum(y2) / len(y2)
	

	days = ["MA", "TI", "KE", "TO", "PE", "LA", "SU"]

	maxBoth = max(max(y1), max(y2))
	
	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	ax1.plot([1,8],[averageY1, averageY1], color = "red", linestyle = "dotted")
	ax1.plot([1,8],[averageY2, averageY2], color = "blue", linestyle = "dotted")
	ax1.plot(x, y1, color="red", marker = "x", markeredgecolor = "red")
	ax1.plot(x, y2, color = "blue", marker = "o", markerfacecolor = "blue")
	
	
	ax1.text(1, maxBoth+4000, "Punainen käyrä: Latausnopeus", fontsize=13)
	ax1.text(1, maxBoth+800, "Sininen käyrä: Lähetysnopeus", fontsize=13)
		
	ax1.set_title(key + ", viikottaiset keskiarvot " + str(resolution) + " tunnin ajalta")
	plt.xlabel("Päivä")
	plt.ylabel("Nopeus(kbps)")
	plt.ylim(0, maxBoth + 7000)
	plt.xticks(range(1,8), days, rotation='vertical')
	plt.xlim(1,8)
	plt.show()



def drawGraphWeek(data, key, resolution):
	x = [1/24 * i[1] + 1 + i[0] for i in data]
	y1 = [i[2] for i in data]
	y2 = [i[3] for i in data]

	days = ["MA", "TI", "KE", "TO", "PE", "LA", "SU"]

	maxBoth = max(max(y1), max(y2))
	
	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	ax1.plot(x, y1, color="red", marker = "o")
	ax1.plot(x, y2, color = "blue", marker = "o")
	
	ax1.text(1, maxBoth+4000, "Punainen käyrä: Latausnopeus", fontsize=13)
	ax1.text(1, maxBoth+800, "Sininen käyrä: Lähetysnopeus", fontsize=13)
		
	ax1.set_title(key + ", viikottaisen keskiarvot " + str(resolution) + " tunnin ajalta")
	plt.xlabel("Päivä")
	plt.ylabel("Nopeus(kbps)")
	plt.ylim(0, maxBoth + 7000)
	plt.xticks(range(1,8), days, rotation='vertical')
	plt.xlim(1,8)
	plt.show()

def drawGraphForOperators(data, postalcode):
	
	elisaX = [i[0] for i in data[0]]
	soneraX = [i[0] for i in data[1]]
	dnaX = [i[0] for i in data[2]]
	elisaY = [i[1] for i in data[0]]
	soneraY = [i[1] for i in data[1]]
	dnaY = [i[1] for i in data[2]]

	maxElisaY = max(elisaY)
	maxDNAY = max(dnaY)
	maxSoneraY = max(soneraY)
	maxAll =max([maxElisaY, maxDNAY, maxSoneraY])

	fig2 = plt.figure()
	ax = fig2.add_subplot(111)
	ax.plot(elisaX, elisaY, color = "red")
	ax.plot(soneraX, soneraY, color = "green")
	ax.plot(dnaX, dnaY, color = "blue")
	ax.grid(True)
	ax.text(1, maxAll + 6700, "Punainen käyrä: Elisa", fontsize=11)
	ax.text(1, maxAll + 3700, "Sininen käyrä: DNA", fontsize=11)
	ax.text(1, maxAll + 700, "Vihreä käyrä: Sonera", fontsize=11)
	plt.ylim(0, maxAll + 10000)
	plt.xlim(0, 24)
	plt.xlabel("Tunti")
	plt.ylabel("Nopeus(kbps)")
	ax.set_title("Data postinumerosta: " + postalcode + ", operaattoreittain")
	plt.show()
	

def drawGraphDay(data, name):

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
	ax1.grid(True)	
	ax1.set_title("Latenssit: " + name)
	plt.ylabel("Ping(ms)")
	plt.xlabel("Hour")

	fig1 = plt.figure()
	ax = fig1.add_subplot(111)
	ax.plot(x1,y1, color = "red", marker = "o")
	ax.plot(x1,y2, color = "blue", marker = "o")
	ax.grid(True)
	plt.ylim(max(0,minY - 7000),maxY + 7000)
	plt.xlim(0, 23)
	ax.set_title("Latausnopeus: " + name + " päivän keskiarvot tunnettain")
	ax.text(int(minX+1), int(maxY+4000), "Red plot: download", fontsize=13)
	ax.text(int(minX+1), int(maxY+600), "Blue plot: upload", fontsize=13)
	plt.xlabel("Hour")
	plt.ylabel("Speed(kbps)")
	plt.show()


'''
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

'''
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
