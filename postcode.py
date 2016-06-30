import csv
import operator
from itertools import groupby
from operator import itemgetter


def getTheBestOperator(code, csvFileName):
	data = getDataFromPostalCodeAndYear(code, "2016", csvFileName)
	data = convertDatasStringToIntOrFloat(data)
	if hasEnoughMeasurements(data):
		if isBigDifferencesInMeasurements(data):
			if hasMostMeasurementsAndHighestDownlink(data):
				return max(data, key=itemgetter(5))[2]
			else:
				data = addSpeedForOperatorsForMeasurements(data)
		if isBigDifferenceInTopSpeed(data):
			if hasHighestDownlinkAndTopSpeed:
				return max(data, key=itemgetter(5))[2]
			else:
				data = addSpeedForOperatorsForTopSpeed(data)
			addSpeedForOperators(data)
		else:
			return max(data, key=itemgetter(5))[2]		


def addSpeedForOperatorsForTopSpeed:
	highestDownlink = max(data, key=itemgetter(5))
	newData = []
		if highestDownlink[4] * 3 < row[4]:
			newData.append((row[0], row[1], row[2], row[3], row[4], row[5] + 3000, row[6]))
		else:
			newData.append(row)
	return newData


def hasHighestDownlinkAndTopSpeed:
	highestDownlink = max(data, key=itemgetter(5)) 
	highestTopSpeed = max(data, key=itemgetter(6))
	return highestDownlink[2] == mostMeasurements[2]

def addSpeedForOperatorsForMeasurements(data):
	highestDownlink = max(data, key=itemgetter(5))
	newData = []
		if highestDownlink[4] * 3 < row[4]:
			newData.append((row[0], row[1], row[2], row[3], row[4], row[5] + 3000, row[6]))
		else:
			newData.append(row)
	return newData

def hasMostMeasurementsAndHighestDownlink(data):
	highestDownlink = max(data, key=itemgetter(5)) 
	mostMeasurements = max(data, key=itemgetter(4))
	return highestDownlink[2] == mostMeasurements[2]


def addSpeedForOperators(data):
	highestSpeed = max(data, key=itemgetter(6)) 
	newData = []
	for row in data:
		print(row)
		if row[6] + 5 < highestSpeed[6]:
			newData.append((row[0], row[1], row[2], row[3], row[4], row[5] + 3000, row[6]))
		 
	for row in newData:
		print(row)
	return data
 
def isBigDifferenceInTopSpeed(data):
	highestSpeed = max(data, key=itemgetter(6))
	lowestSpeed = min(data, key=itemgetter(6))
	return lowestSpeed[6] + 5 < highestSpeed[6]

def isBigDifferencesInMeasurements(data):
	mostMeasurements = max(data, key=itemgetter(4))
	fewestMeasurements = min(data, key=itemgetter(4))
	return fewestMeasurements[4] * 3 < mostMeasurements[4]
	
	


def convertDatasStringToIntOrFloat(data):
	converted = []
	for row in data:
		converted.append((row[0], row[1], row[2], row[3], int(row[4]), float(row[5]), float(row[6])))
	return converted		


def getBestOperatorFromYearAndCode(year, code, csvFileName):
	data = getDataFromPostalCodeAndYear(code, year, csvFileName)
	operators = ["DNA", "Sonera", "Elisa"]
	collected = []
	for row in data:
		if row[1] == year:
			collected.append((row[2], float(row[5])))
	
	best = ["Couldn't find the best operator from this area!"]
	for line in collected:
		newBest = max(collected, key=itemgetter(1))
		if newBest[0] in operators:
			best = newBest

	return best[0]


#def hasChanged(operator, startYear, endYear, data):
	

#def getEnoughForOperatorWithLittleData(data, csvFileName):
	

def hasEnoughMeasurements(data):
	if len(data) != 0:
		return all(int(i[4]) >50 for i in data)
	else:
		return False

			
'''
def getBestOperator(csvFileName):
	collected = []
	for code in range(10000, 20000, 10):
		collected.append(getBestOperatorFromYearAndCode("2015", str(code), csvFileName))
	print (collected[10])
	return collected
'''

def getDataFromPostalCodeAndYear(code, year, csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		collected = []
		for row in reader:	
			if row[0] == code and row[1] == year:
				collected.append(row)
	return collected
	
'''
def removeFalseRows(csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		with open("correctpostcodecsv.csv", "w") as newCSV:
			writer = csv.writer(newCSV)
			for row in reader:
				if row[2] != "undefined":
					writer.writerow(row)
'''					


'''
def createBettercsv(csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		with open("postcodecsv.csv", "w") as newCSV:
			writer = csv.writer(newCSV)
			writer.writerow(next(reader))
			for row in reader:
				if len(row[0]) == 3:
					newCode = "00" + row[0]
					writer.writerow([newCode, row[1], row[2], row[3], row[4], row[5], row[6]])
				elif len(row[0]) == 4:
					newCode = "0" + row[0]
					writer.writerow([newCode, row[1], row[2], row[3], row[4], row[5], row[6]])
				else:
					writer.writerow(row)

'''








	

