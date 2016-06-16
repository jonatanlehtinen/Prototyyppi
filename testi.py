import csv
import operator

def calculateAverageDownlink(csvFileName):
	with open(csvFileName) as testfile:
		target = open('kohde.csv', 'w')
		reader = csv.reader(testfile)
		writer = csv.writer(target)
		reader.next()
		count = 0
		allDowns = 0.0
		for row in reader:
			if row[15]:	
				count += 1
				allDowns += float(row[15])
		#writer.writerow(["Average downlink"])
		#writer.writerow([allDowns/count])
	
	
	return str(allDowns/count) 
	testfile.close

def getHighestDownlinkWithDevice(csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		reader.next()
		collected = []
		for row in reader:
			collected.append((row[2] + " " + row[3], float(row[15])))
		sortedList = sorted(collected, key=lambda tup: tup[1], reverse = True)
		#sortedlist = sorted(reader, key=operator.itemgetter(15), reverse=True)
		#for row in sortedlist:
			#print row[3] + "  " + row[15]		
		#device = ""
		#for row in reader: 			
		#	if (row[15] and (float(row[15]) > currentBest)):
		#		currentBest = float(row[15])
		#		device = row[2] + " " + row[3]			
	
	return sortedList[0][0] + " " + str(sortedList[0][1])
	csvFile.close

	










