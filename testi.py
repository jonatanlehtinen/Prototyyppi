import csv
import operator
from itertools import groupby
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
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
	x,y = map(lon, lat)
	map.plot(x,y, 'bo', markersize = 4)
	#map.drawmeridians(np.arange(0, 360, 30))
	#map.drawparallels(np.arange(-90, 90, 30))
	 
	plt.show()

def getAverageDownlink(csvFileName):
	with open(csvFileName) as testfile:
		reader = csv.reader(testfile)
		downlinkIndex = getIndexOfColumn(csvFileName, "16-downlink")
		next(reader)
		count = 0
		allDowns = 0.0
		for row in reader:
			if row[downlinkIndex]:	
				count += 1
				allDowns += float(row[downlinkIndex])
	return allDowns/count


def getHighestDownlinkWithDevice(csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		vendorIndex = getIndexOfColumn(csvFileName, "3-vendor")
		modelIndex = getIndexOfColumn(csvFileName, "4-model")
		downlinkIndex = getIndexOfColumn(csvFileName, "16-downlink")
		techTypeIndex = getIndexOfColumn(csvFileName, "26-radiotype")
		next(reader)
		collected = []
		for row in reader:
			if row[vendorIndex] and row[modelIndex] and row[downlinkIndex] and row[techTypeIndex] == "cell":
				collected.append((row[vendorIndex] + " " + row[modelIndex], float(row[downlinkIndex])))
		sortedList = sorted(collected, key=lambda tup: tup[1], reverse = True)		
	return sortedList[0][0] + " " + str(sortedList[0][1])


def getBestAveragePhone(csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		next(reader)
		vendorIndex = getIndexOfColumn(csvFileName, "3-vendor")
		modelIndex = getIndexOfColumn(csvFileName, "4-model")
		downlinkIndex = getIndexOfColumn(csvFileName, "16-downlink")
		radioTypeIndex = getIndexOfColumn(csvFileName, "26-radiotype")
		collected = []
		for row in reader:
			if row[vendorIndex] and row[modelIndex] and row[downlinkIndex] and row[radioTypeIndex] == "cell":
				collected.append((row[vendorIndex] + " " + row[modelIndex], float(row[downlinkIndex])))		
		sortedList = sorted(collected, key=lambda tup: tup[0], reverse = True)	
		count = 0
		counted = 0
		holder = []	
		for key, group in groupby(sortedList, lambda x: x[0]):
			for row in group:
				count += 1
				counted += row[1]
			holder.append((key, counted/count))			
			counted = 0
			count = 0

	best = max(holder, key=itemgetter(1))
	return best[0] + " " + str(best[1])
	

def getDataFromDate(date, csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		dateIndex = getIndexOfColumn(csvFileName, "1-startedAt")
		next(reader)	
		filteredList = filter(lambda x: x[dateIndex][:10] == date, list(reader))
	return filteredList


def getBestByPostalcode(postalcode, csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		next(reader)
		vendorIndex = getIndexOfColumn(csvFileName, "3-vendor")
		modelIndex = getIndexOfColumn(csvFileName, "4-model")
		downlinkIndex = getIndexOfColumn(csvFileName, "16-downlink")
		radioTypeIndex = getIndexOfColumn(csvFileName, "26-radiotype")
		collected = []
		for row in reader:
			if row[47] and row[47] == postalcode and row[vendorIndex] and row[modelIndex] and row[downlinkIndex] and row[radioTypeIndex] == "cell":
				collected.append((row[vendorIndex], row[modelIndex], float(row[downlinkIndex]), "cell"))
		sortedList = sorted(collected, key=lambda x: x[2], reverse = True)
		header = (["3-vendor", "4-model", "16-downlink", "26-radiotype"])	
		createCSV(header, sortedList)
	return getBestAveragePhone("csvfiletest.csv")
		

def getIndexOfColumn(csvFileName, wantedColumn):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		index = list(reader)[0].index(wantedColumn)
	return index


def createCSV(header, data):
	with open("csvfiletest.csv", "w") as newcsvfile:
		writer = csv.writer(newcsvfile)
		writer.writerow(header)
		writer.writerows(data)
	  

def getDataFromPostalCode(code, csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		collected = []
		for row in reader:
			if str(row[0]) == code:
				print("ssdg")
				collected.append(row)
		print (collected)




	










