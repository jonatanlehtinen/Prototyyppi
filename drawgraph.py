import matplotlib.pyplot as plt
import pylab
import mysql.connector as mariadb
import datetime

def drawGraph():

	data = getAverages()
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
	plt.xlabel("Time")
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


