import csv
import operator
from itertools import groupby
from operator import itemgetter

def getBestOperatorFromYearAndCode(year, code, csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		data = getDataFromPostalCode(code, csvFileName)
		collected = []
		for row in data:
			if row[1] == year:
				collected.append((row[2], float(row[5])))

	best = max(collected, key=itemgetter(1))
	return best[0]
				


def getDataFromPostalCode(code, csvFileName):
	with open(csvFileName) as csvFile:
		reader = csv.reader(csvFile)
		collected = []
		for row in reader:	
			if row[0] == code:
				collected.append(row)
	return collected
	

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








	

