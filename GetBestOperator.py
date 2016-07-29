import csv
import operator
from itertools import groupby
from operator import itemgetter
import mysql.connector as mariadb

#Connect to database and return wanted data by postcode
def getFromDataBase(code):
	try:
		#Create connection to database
		mariadb_connection = mariadb.connect(user='root', password='pythontesti', database='postcodes')
		cursor = mariadb_connection.cursor()
		
		#Query for right data
		cursor.execute("SELECT postcode, year, operator, downloadMeasurements, averageDownload, topDownload, uploadMeasurements, averageUpload, topUpload, confidenceIntervalMin, confidenceIntervalMax FROM postcode WHERE postcode=%s", (code,))
		mariadb_connection.close()
		
		#return list including fetched data
		return list(cursor)
	except:
		print("Couldn't create database connection")
		return []


'''
Method for fetching data from database when calculating
limits for confidence intervals
'''
def getFromDataBaseForIntervalCalculation():
	try:
		#Create connection to database
		mariadb_connection = mariadb.connect(user='root', password='pythontesti', database='postcodes')
		cursor = mariadb_connection.cursor()
		
		#Query for right data
		cursor.execute("SELECT postcode, year, operator, downloadMeasurements, averageDownload, topDownload, uploadMeasurements, averageUpload, topUpload, confidenceIntervalMin, confidenceIntervalMax FROM postcode",)
		mariadb_connection.close()
		
		#return list including fetched data
		return list(cursor)
	except:
		print("Couldn't create database connection")
		return []

'''
Main method for calculating the best operator 
from given parameter list of postcodes, returns
list of lists. Every lists first element is operators name,
second element is postcode, third is points from this
postcode and then comes the amount of confidence points.
This postcode-points-confidencepoints-combo repeats itself
as many times as there are postcodes(presuming operator has
data from every postcode) and the last element is the average
points.
'''
def getTheBestOperator(codes):
	#variable where points are added and 
	points = []
	#loop through postcodes
	for code in codes:
		#Calculate points for every operator from that postcode
		pointsFromCode = calculatePointsFromCode(code)
		#loop through operators which points where calculated
		for operator in pointsFromCode:
			#if operators hasn't already being added to variable points
			#it will be added now 
			if operator not in [i[0] for i in points]:
				#for the first time, add this operator, postcode,
				# scoring points and confidence points to variable points 
				points.append([operator, code, pointsFromCode[operator][0], pointsFromCode[operator][1]])
			else:
				#operator has alreada being added to variable points
				#so find out where it is and append next postcode to its list
				temp = [i[0] for i in points].index(operator)
				points[temp].append(code)
				points[temp].append(pointsFromCode[operator][0])
				points[temp].append(pointsFromCode[operator][1])
	#loop through points and add average amount of points
	#for operators to the end of every list
	for operator in points:
		length = len(operator)
		i = 2
		collectedPoints = []
		while i < length:
			collectedPoints.append(operator[i])
			i += 3
		operator.append(sum(collectedPoints) / len(collectedPoints))
	
	return points


'''
This method calculates points for operators and returns
dictionary with every operator as its keys and lists of points
as its items. Lists contain two elements, the first element is
the amount of points operator has scored from the given postcode
and the second element is the amount of confidence points
operator gets from the given postcode
'''
def calculatePointsFromCode(code):
	#Get data from database
	data = getFromDataBase(code)
	operators = []
	
	for row in data:
		operators.append(row[2])
	operators = set(operators)

	#Variable for keeping score of points given for operators
	operatorsPoints = dict.fromkeys(operators,0.0)

	#Check if some operators don't have enough measurements
	#and add more from past if they are missing
	addedData, operatorsPoints = getMoreData(data, operatorsPoints)
	
	#Do some point calculations and return the best operator	
	operatorsPoints = gradeOperators(addedData, operatorsPoints)

	#Add confidence points for every operator 
	operatorsPoints = addConfidencePoints(addedData, operatorsPoints)

	return operatorsPoints




'''
this method adds more data for operators who have
fewer than 50 measurements. This method also increments
operators points according to the age of data. 
return tuple with two elements, first element is list of
every operator which have data from wanted postcode and 
operators have atleast 50 measurements if they have that much 
measurements from this postcode. If data had to be fetched 
from past, weighted average calculations have been perfomed.
Second element is holding updated points for operators.
'''
def getMoreData(data, operatorsPoints):
	
	#Variable to hold operators with enough data
	operatorsToAddData = []
	updatedPoints = operatorsPoints

	#Variable to hold operators with enough data
	operatorsHavingEnoughData = []
	
	#sort data first by operator's name, then by year
	data.sort(key=lambda x: (x[2], x[1]), reverse = True)
	
	#Variable to hold operators which are already added to 
	#either operatorsToAddData or operatorsHavingEnoughData
	addedOperators = []

	#loop through every line in data
	for row in data:
		#add operator to operatorsToAddData or operatorsHavingEnoughData
		#depending on the amount of measurements and if operator has already being added.
		#Also points for operators are being incremented according to the age of data.
		if row[2] not in addedOperators:
			addedOperators.append(row[2])
			if row[3] <= 50:			
				operatorsToAddData.append(row)
			elif row[1] == 2016 and row[3] > 50:
				operatorsHavingEnoughData.append(row)
				updatedPoints[row[2]] = 2
			elif row[1] == 2015 and row[3] > 50:
				operatorsHavingEnoughData.append(row)
				updatedPoints[row[2]] = 1
			elif row[1] == 2014 and row[3] > 50:
				operatorsHavingEnoughData.append(row)
				updatedPoints[row[2]] = 0.5
			elif row[1] == 2013 and row[3] > 50:
				operatorsHavingEnoughData.append(row)
	
	
	count = 0
	collected = []
	year = 2015
	
	#if every operator has more than 50 measurements during 2016
	#there is no need to add any data. If even one operator has 
	#not enough measurements, while loop is initiated
	if len(operatorsToAddData) == 0:
		notEnoughData = False
	else:
		notEnoughData = True 
	
	#loop to add data for operators lacking it. This won't be
	#needed if every operators has more than 50 measurements.
	while(notEnoughData and year > 2012):
		count = 0

		#loop through every operator having inadequate data.
		for operator in operatorsToAddData:

			#loop through every line in data
			for row in data:

				#If match is found, add to variable collected
				if row[1] == year and row[2] == operator[2]:
					collected.append(row)
			
			#Determine if operator has already being added to 
			#operatorsHavingEnoughData
			isNotAlreadyInList = True
			for row in operatorsHavingEnoughData:
				if operator[2] == row[2]:
					isNotAlreadyInList = False

			if collected:
				
				#if something was found during first loop, calculate weighted average
				#from operators data and collected
				weightedAverageData = calculateWeightedAverage(collected[0], operator)

				#If newly calculated data has more than 50 measurements and operator
				# hasn't been added in operatorsHavingEnoughData, add it now and
				#and increment points according to the age of data 
				if weightedAverageData[3] > 50 and isNotAlreadyInList:
					operatorsHavingEnoughData.append(weightedAverageData)
					if year == 2015:
						updatedPoints[weightedAverageData[2]] = 1
					elif year == 2014:
						updatedPoints[weightedAverageData[2]] = 0.5	

				#else update operatorsToAddData with newly calculated data		
				else:
					operatorsToAddData[count] = weightedAverageData

			#if this is last while loop(year = 2013) and operator hasn't already being added
			#to operatorsHavingEnoughData, add it now
			if year == 2013 and isNotAlreadyInList:
				operatorsHavingEnoughData.append(operatorsToAddData[count])
			collected = []
			count += 1
		year -= 1
			
	return (operatorsHavingEnoughData, updatedPoints)



'''
mittaustenmäärä1*latausmäärä1 + mittaustenmäärä2*latausmäärä2/(mittaustenmäärä1+mittaustenmäärä2)
'''


'''
calculates weighted average for download and upload speeds
and adds measurements from older data. Returns new tuple
where averages and measurements are updated.
'''
def calculateWeightedAverage(data1, data2):	
	
	#Check that data isn't from the same year
	if data1[1] != data2[1]:
		
		#calculate weighted average for download speed
		weightedDownloadSpeed = (data1[3] * data1[4] + data2[3] * data2[4]) / (data1[3] + data2[3])

		#calculate weighted average for upload speed
		weightedUploadSpeed = (data1[6] * data1[7] + data2[6] * data2[7]) / (data1[6] + data2[7])
		newData = list(data2)

		#update information
		newData[4] = weightedDownloadSpeed
		newData[7] = weightedUploadSpeed
		newData[3] = data1[3] + data2[3]
		newData[6] = data1[6] + data2[6]
		return tuple(newData)
	else:
		return data2 
	

'''
Method for grading the operators. Operators grade is
calculated by adding to the amount of points they were
given regarding to the age and amount of data they had
points from three categories: average download speed,
average upload speed and maximum download speed. Points
from these categories are determined by relation between
the best operator and the rest. For example from average
download speed the points are calculated followingly:
4 * max(averageDownload) / operatorsDownload. So the 
best operator by average download speed will be given
maximum 4 points and the other operators points depend
on their average download speed relation between the best.
'''
def gradeOperators(data, operatorsPoints):

	#Calculate max values
	maxAverageDown = max([i[4] for i in data])
	maxAverageUp = max([i[7] for i in data])
	maxDown = max([i[5] for i in data])

	#Calculate points for every operator
	for operator in data:
		#Calculate factors
		aveDownFactor = operator[4] / maxAverageDown
		aveUpFactor = operator[7] / maxAverageUp
		downFactor = operator[5] / maxDown
		
		#add points for operators
		operatorsPoints[operator[2]] += aveDownFactor *  4
		operatorsPoints[operator[2]] += aveUpFactor *  1
		operatorsPoints[operator[2]] += downFactor * 1
	
	return operatorsPoints
	
'''
add points for operators from the amount of confidence
of their data. This method calculates confidence points for 
operators and adds it to the variable operatorsPoints which
is returned. 
'''
def addConfidencePoints(data, operatorsPoints):

	#get the limits for points
	limits = calculateLimits()
	#loop through parameter data, which contains
	#operators data from one postcode
	for datarow in data:
		#interval = confidence max - confidence min
		interval = datarow[10] - datarow[9]
		points = 5
		notAdded = True
		#loop through the limits for the points
		for limit in limits:
			#if operators interval is smaller than the limit
			#and operators points hasn't already being added
			#they shall be added now 
			if interval < limit and notAdded:
				#for current operator add confidence points
				operatorsPoints[datarow[2]] = [operatorsPoints[datarow[2]], points]
				notAdded = False			
			points -= 1
		#if operator was not added or in other words its confidence
		#interval doesn't suffice for even 1 point, zero will be added
		if notAdded:
			operatorsPoints[datarow[2]] = [operatorsPoints[datarow[2]], 0]

	return operatorsPoints


'''
add points for operators from the amount of confidence
of their data. This method calculates confidence points for 
operators and adds it to the variable operatorsPoints which
is returned. 
'''
def addConfidencePoints(data, operatorsPoints):

	#get the limits for points
	limits = calculateLimits()
	#loop through parameter data, which contains
	#operators data from one postcode
	for datarow in data:
		#interval = confidence max - confidence min
		interval = datarow[10] - datarow[9]
		points = 5
		notAdded = True
		#loop through the limits for the points
		for limit in limits:
			#if operators interval is smaller than the limit
			#and operators points hasn't already being added
			#they shall be added now 
			if interval < limit and notAdded and interval != 0.0:
				#for current operator add confidence points
				operatorsPoints[datarow[2]] = [operatorsPoints[datarow[2]], points]
				notAdded = False			
			points -= 1
		#if operator was not added or in other words its confidence
		#interval doesn't suffice for even 1 point, zero will be added
		if notAdded:
			operatorsPoints[datarow[2]] = [operatorsPoints[datarow[2]], 0]

	return operatorsPoints



'''
Calculates limits for confidence scores. Returns list 
of floats where the first element is the minimum amount
of confidence level which is required to get 5 out of 5
points, the second element is the minimum amount for 4
points and so on. Confidence levels are determined by 
bell curve: every confidence interval is being calculated
from data and then sorted from the smallest to the highest.
The smaller the interval the better the points. Top 15% is 
being given 5 points, 20% will be given 4 and so on.  

'''
def calculateLimits():
	#get all data from database
	data = getFromDataBaseForIntervalCalculation()
	#calculate the intervals for data by subtracting the 
	#confidence intervals max amount from the min amount
	intervals = [i[10] - i[9] for i in data if i[3] > 1 and i[9] != 0.0 and i[10] != 0.0]
	#sort from smallest to highest
	srtd = sorted(intervals)
	lengthOfList = len(srtd)
	#set percentages for each point
	fivePointPercentage = 0.15
	fourPointPercentage = 0.20
	threePointPercentage = 0.20
	twoPointPercentage = 0.25
	onePointPercentage = 0.15
	zeroPointPercentage = 0.5
	#calculate the amount operators which will be given wanted points
	amountOfFivePoint = round(lengthOfList * fivePointPercentage)
	amountOfFourPoint = round(lengthOfList * fourPointPercentage)
	amountOfThreePoint = round(lengthOfList * threePointPercentage)
	amountOfTwoPoint = round(lengthOfList * twoPointPercentage)
	amountOfOnePoint = round(lengthOfList * onePointPercentage)
	amountOfZeroPoint = lengthOfList - amountOfFivePoint - amountOfFourPoint - amountOfThreePoint - amountOfTwoPoint - amountOfOnePoint
	#get the limits from data
	fivePointMax = srtd[amountOfFivePoint]
	fourPointMax = srtd[amountOfFourPoint + amountOfFivePoint]
	threePointMax = srtd[amountOfThreePoint + amountOfFourPoint + amountOfFivePoint]
	twoPointMax = srtd[amountOfTwoPoint + amountOfThreePoint + amountOfFourPoint + amountOfFivePoint]
	onePointMax = srtd[amountOfOnePoint + amountOfTwoPoint + amountOfThreePoint + amountOfFourPoint + amountOfFivePoint]

	return[round(fivePointMax), round(fourPointMax), round(threePointMax), round(twoPointMax), round(onePointMax)]

'''
this method was used when calculating the confidence intervals
for data. Parameter data is containing data from one operator
from one postcode from 2016.
'''
def calculateIntervals(data):
	count = 0
	rowAmount = len(data)
	#loop through
	for row in data:
		count += row[0]
	#if there's not enough rows return 0.0,0.0
	if rowAmount < 2:
		return(0.0,0.0)
	else:	
		#calculate operators average download speed
		average = count/rowAmount
		count = 0
		#calculate standard deviation
		for row in data:
			count += (row[0] - average) ** 2	
		count = count * (1/(rowAmount-1))
		standardDeviation = math.sqrt(count)
		#define the precision of confidence interval, here 99%
		qt = norm.ppf(0.99)	
		#calculate minimum and maximum limits and return them
		value1 = average - qt * (standardDeviation/math.sqrt(rowAmount))
		value2 = average + qt * (standardDeviation/math.sqrt(rowAmount))
		return(value1, value2)

'''
This method converts data's wanted strings to int or float
and returns new list containing converted tuples
'''
'''
def convertDatasStringToIntOrFloat(data):
	converted = []
	for row in data:
		converted.append((row[0], row[1], row[2], int(row[3]), float(row[4]), float(row[5]), int(row[6]), float(row[7]), float(row[8])))	
	return converted
'''	

if __name__ == '__main__':
	print(getTheBestOperator(["02600","00100"]))
					
'''
def calculateBestOperator(data):
	if hasMostMeasurementsAndHighestDownlink(data):
		return max(data, key=itemgetter(5))[2]
	else:
		data = addSpeedForOperatorsForMeasurements(data)
		data = addSpeedForOperatorsForTopSpeed(data)
		return max(data, key=itemgetter(5))[2]
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
	
	
def hasEnoughMeasurements(data):
	if len(data) != 0:
		return all(int(i[3]) > 50 for i in data)
	else:
		return False
			
def getBestOperator(csvFileName):
	collected = []
	for code in range(10000, 20000, 10):
		collected.append(getBestOperatorFromYearAndCode("2015", str(code), csvFileName))
	print (collected[10])
	return collected
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
	
def getData(data):
	with open("correctpostcodecsv.csv") as csvFile:
		reader = csv.reader(csvFile)
		returnValue = []
		for row in reader:
			if row[0] == data[0] and row[1] == data[1]  and row[2]==data[2]:
				returnValue = [row[4], row[5], row[6]] 
	return returnValue
		

		
def createOfficialCSV():
	with open("result.csv") as csvFile:
		with open("mycsv1.csv") as secondCSV:		
			with open("newestresult.csv", "w") as newCSV:
				reader1 = csv.reader(csvFile)
				reader2 = csv.reader(secondCSV)
				next(reader2)
				listana = list(reader2)
				writer = csv.writer(newCSV)
				for row in reader1:
					writer.writerow(row)
					if int(row[3]) <= 50:
						notEnoughData = True
						year = 2015
						amount = int(row[3])
						while notEnoughData and year > 2012:
							for row1 in listana:
								if(row1[0] == row[0] and row1[1] == str(year) and row[2] == row1[2]):
									amount += int(row1[4])
								if(amount > 50 and notEnoughData):
									writer.writerow(row1[:3] + row1[4:] + [0.0, 0.0])
									notEnoughData = False
							year -= 1
				
		
	
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




