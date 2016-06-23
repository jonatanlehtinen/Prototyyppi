import csv
import operator
from itertools import groupby
from operator import itemgetter


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
	testfile.close	
	return allDowns/count


def getHighestDownlinkWithDevice(csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		vendorIndex = getIndexOfColumn(csvFileName, "3-vendor")
		modelIndex = getIndexOfColumn(csvFileName, "4-model")
		downlinkIndex = getIndexOfColumn(csvFileName, "16-downlink")
		next(reader)
		collected = []
		for row in reader:
			collected.append((row[vendorIndex] + " " + row[modelIndex], float(row[downlinkIndex])))
		sortedList = sorted(collected, key=lambda tup: tup[1], reverse = True)		
	return sortedList[0][0] + " " + str(sortedList[0][1])
	csvFile.close

def getBestAveragePhone(csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		next(reader)
		vendorIndex = getIndexOfColumn(csvFileName, "3-vendor")
		modelIndex = getIndexOfColumn(csvFileName, "4-model")
		downlinkIndex = getIndexOfColumn(csvFileName, "16-downlink")
		sortedList = []
		collected = []
		for row in reader:
			collected.append((row[vendorIndex] + " " + row[modelIndex], float(row[downlinkIndex])))
		sortedList = sorted(collected, key=lambda tup: tup[0], reverse = True)	
		count = 0
		counted = 0
		holder = []	
		for key, group in groupby(sortedList, lambda x: x[0]):
			#print (key)
			print (",".join(str(list(group)[0][1])))
			for row in group:
				print (row)
				count += 1
				counted += row[1]
			holder.append((key, counted/count))			
			counted = 0
			count = 0

	best = max(holder, key=itemgetter(1))
	csvFile.close
	return best[0] + " " + str(best[1])
	

def getDataFromDate(date, csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		dateIndex = getIndexOfColumn(csvFileName, "1-startedAt")
		next(reader)	
		filteredList = filter(lambda x: x[dateIndex][:10] == date, list(reader))
	csvFile.close	
	return filteredList

def getBestByPostalcode(postalcode, csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		next(reader)
		vendorIndex = getIndexOfColumn(csvFileName, "3-vendor")
		modelIndex = getIndexOfColumn(csvFileName, "4-model")
		downlinkIndex = getIndexOfColumn(csvFileName, "16-downlink")
		collected = []
		for row in reader:
			if row[47] == postalcode:
				collected.append((row[vendorIndex], row[modelIndex], float(row[downlinkIndex])))
		sortedList = sorted(collected, key=lambda x: x[2], reverse = True)
		header = (["3-vendor", "4-model", "16-downlink"])	
		createCSV(header, sortedList)
		'''with open("csvfiletest.csv", "w") as newcsvfile:
			writer = csv.writer(newcsvfile)	
			writer.writerow(["3-vendor", "4-model", "16-downlink"])	
			for row in sortedList:
				writer.writerow([row[0], row[1], row[2]])
		newcsvfile.close
		'''
	csvFile.close
	return getBestAveragePhone("csvfiletest.csv")
		

def getIndexOfColumn(csvFileName, wantedColumn):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		index = list(reader)[0].index(wantedColumn)
	csvFile.close
	return index


def createCSV(header, data):
	with open("csvfiletest.csv", "w") as newcsvfile:
		writer = csv.writer(newcsvfile)
		writer.writerow(header)
		writer.writerows(data)
	  






	










