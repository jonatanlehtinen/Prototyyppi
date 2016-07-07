import csv
import operator
from itertools import groupby
from operator import itemgetter
import mysql.connector as mariadb


def getFromDataBase(code):
	try:
		mariadb_connection = mariadb.connect(user='root', password='pythontesti', database='postcodes')
		cursor = mariadb_connection.cursor()
		cursor.execute("SELECT postcode, year, operator, downloadMeasurements, averageDownload, topDownload, uploadMeasurements, averageUpload, topUpload FROM correctpostcode WHERE postcode=%s", (code,))
		mariadb_connection.close()
		return list(cursor)
	except:
		print("Couldn't create database connection")
		return []

		

def getTheBestOperator(code, csvFileName):
	data = getFromDataBase(code)
	operators = []
	for row in data:
		operators.append(row[2])
	operators = set(operators)
	operatorsPoints = dict.fromkeys(operators,0.0)
	data = convertDatasStringToIntOrFloat(data)
	dataFrom2016 = []
	for row in data:
		if row[1] == "2016":
			dataFrom2016.append(row)
	year = 2015
	dataFrom2016 = getMoreData(data, operatorsPoints)
	print(dataFrom2016[0])
	
	#while(not hasEnoughMeasurements(dataFrom2016) and year > 2012):
	#	dataFrom2016 = getMoreData(data)
	#	year -= 1
		#print ("moikkamoi")
	if hasEnoughMeasurements(dataFrom2016[0]):
		print("moikkamoi")
		return calculateBestOperator(dataFrom2016[0])
	
	else:
		'''
		data2 = getDataFromPostalCodeAndYear(code, "2015", csvFileName)
		data2 = convertDatasStringToIntOrFloat(data2)
		firstBest = calculateBestOperator(data)
		secondBest = calculateBestOperator(data2)
		if firstBest == secondBest:
			return max(data, key=itemgette(5))[2]
		else: 
			return getBestOperatorFromTwoYearByMeasurements(data, data2, firstBest, secondBest)
		'''
		return "Not enough measurements, couldn't determine the best operator."


def getMoreData(data, operatorsPoints):
	operatorsToAddData = []
	updatedPoints = operatorsPoints
	operatorsHavingEnoughData = []
	data.sort(key=lambda x: (x[2], x[1]), reverse = True)
	addedOperators = []
	for row in data:
		if row[2] not in addedOperators:
			addedOperators.append(row[2])
			if row[3] <= 50:			
				operatorsToAddData.append(row)
			elif row[1] == "2016" and row[3] > 50:
				operatorsHavingEnoughData.append(row)
				updatedPoints[row[2]] = 2
			elif row[1] == "2015" and row[3] > 50:
				operatorsHavingEnoughData.append(row)
				updatedPoints[row[2]] = 1
			elif row[1] == "2014" and row[3] > 50:
				operatorsHavingEnoughData.append(row)
				updatedPoints[row[2]] = 0.5
			elif row[1] == "2013" and row[3] > 50:
				operatorsHavingEnoughData.append(row)
	
		

	#for key, group in groupby(data, lambda x: x[2]):
			#print(key)
			#print(max(group, key=itemgetter(1)))
	#		for row in group:
	#
	'''
	for row in data:
		if row[3] <= 50 and row[1]=="2016":			
			operatorsToAddData.append(row)
		elif row[1] == "2016" and row[3] > 50:
			operatorsHavingEnoughData.append(row)
			updatedPoints[row[2]] = 2
	'''
	count = 0
	operatorsInDict = {}
	collected = []
	year = 2015
	if len(operatorsToAddData) == 0:
		notEnoughData = False
	else:
		notEnoughData = True 
	#for row in operatorsToAddData:
		#print("asdf")		
		#print(row)
	while(notEnoughData and year > 2012):
		count = 0
		for operator in operatorsToAddData:
			for row in data:
				if row[1] == str(year) and row[2] == operator[2]:
					collected.append(row)
			
			isNotAlreadyInList = True
			for row in operatorsHavingEnoughData:
				if operator[2] == row[2]:
					isNotAlreadyInList = False
			if collected:
				weightedAverageData = calculateWeightedAverage(collected[0], operator)

				if weightedAverageData[3] > 50 and isNotAlreadyInList:
					operatorsHavingEnoughData.append(weightedAverageData)
					if year == 2015:
						updatedPoints[weightedAverageData[2]] = 1
					elif year == 2014:
						updatedPoints[weightedAverageData[2]] = 0.5			
				else:
					operatorsToAddData[count] = weightedAverageData

			if year == 2013 and isNotAlreadyInList:
				operatorsHavingEnoughData.append(operatorsToAddData[count])
			collected = []
			count += 1
		year -= 1
	#for row in operatorsToAddData:
	#	print("asdf222")
	#	print(row)
			
	return (operatorsHavingEnoughData, updatedPoints)

def getBestOperatorFromTwoYearByMeasurements(data, data2, firstBest, secondBest):
	firstMeasurements = 0
	secondMeasurements = 0	
	for row in data:
		if row[2] == firstBest:
			firstMeasurements = int(row[4])
	for row in data2:
		if row[2] == secondBest:
			secondMeasurements = int(row[4])

	if firstMeasurements > secondMeasurements:
		return firstBest
	elif secondMeasurements > firstMeasurements:
		return secondBest
	else:
		return "Tie between" + firstBest + " and " + secondBest

'''
mittaustenmäärä1*latausmäärä1 + mittaustenmäärä2*latausmäärä2/(mittaustenmäärä1+mittaustenmäärä2)
'''

def calculateWeightedAverage(data1, data2):	
	
	#print(data1)
	#print("asdf")
	#print(data2)
	if data1[1] != data2[1]:
		weightedDownloadSpeed = (data1[3] * data1[4] + data2[3] * data2[4]) / (data1[3] + data2[3])
		newData = list(data2)
		newData[4] = weightedDownloadSpeed
		newData[3] = data1[3] + data2[3]
		#print(newData)
		return tuple(newData)
	else:
		return data2


def calculateBestOperator(data):
	if hasMostMeasurementsAndHighestDownlink(data):
		return max(data, key=itemgetter(5))[2]
	else:
		data = addSpeedForOperatorsForMeasurements(data)
		data = addSpeedForOperatorsForTopSpeed(data)
		return max(data, key=itemgetter(5))[2]

'''
def calculateBestOperator(data):
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
			return max(data, key=itemgetter(5))[2]
	else:
		return max(data, key=itemgetter(5))[2]	
'''

def addSpeedForOperatorsForTopSpeed(data):
	highestDownlink = max(data, key=itemgetter(5))
	newData = []
	for row in data:
		if highestDownlink[6] + 5000 < row[6]:
			newData.append((row[0], row[1], row[2], row[3], row[4], row[5] + 2000, row[6]))
		else:
			newData.append(row)
	return newData


def hasHighestDownlinkAndTopSpeed(data):
	highestDownlink = max(data, key=itemgetter(5)) 
	highestTopSpeed = max(data, key=itemgetter(6))
	return highestDownlink[2] == mostMeasurements[2]

def addSpeedForOperatorsForMeasurements(data):
	highestDownlink = max(data, key=itemgetter(5))
	newData = []
	for row in data:
		if highestDownlink[4] * 3 < row[4]:
			newData.append((row[0], row[1], row[2], row[3], row[4], row[5] + 3000, row[6]))
		else:
			newData.append(row)
	return newData

def hasMostMeasurementsAndHighestDownlink(data):
	highestDownlink = max(data, key=itemgetter(5)) 
	sortedByMeasurements = sorted(data, key=lambda x: x[4], reverse=True)
	mostMeasurements = max(data, key=itemgetter(5)) 
	if sortedByMeasurements[1][4] * 3 < sortedByMeasurements[0][4] and highestDownlink[2] == mostMeasurements[2]:
		return True
	else:
		return False



def addSpeedForOperators(data):
	highestSpeed = max(data, key=itemgetter(6)) 
	newData = []
	for row in data:
		if row[6] + 5 < highestSpeed[6]:
			newData.append((row[0], row[1], row[2], row[3], row[4], row[5] + 3000, row[6]))
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
		converted.append((row[0], row[1], row[2], int(row[3]), float(row[4]), float(row[5]), int(row[6]), float(row[7]), float(row[8])))	
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
		return all(int(i[3]) > 50 for i in data)
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
	

def removeFalseRows(csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		with open("correctpostcodecsv1.csv", "w") as newCSV:
			writer = csv.writer(newCSV)
			for row in reader:
				if row[2] != "undefined":
					writer.writerow(row)


def testRead(csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		print(next(reader))
		print(next(reader))
	
'''
def getData(data):
	with open("correctpostcodecsv.csv") as csvFile:
		reader = csv.reader(csvFile)
		returnValue = []
		for row in reader:
			if row[0] == data[0] and row[1] == data[1]  and row[2]==data[2]:
				returnValue = [row[4], row[5], row[6]] 
	return returnValue
		
	

		
def createOfficialCSV(csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		next(reader)
		with open("mycsv1.csv", "w") as mycsv:
			writer = csv.writer(mycsv)
			for row in reader:
				dataToAdd = getData(row)
				writer.writerow(row + dataToAdd)
				
				


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









	

