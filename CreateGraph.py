import getAverage as calc
import datetime
from drawgraph import *
import sys

def createWantedGraph(time,key,location,typeOfLocation,longTime,weekly,fir,timeWindow,resolution,sortOperators,filename):
	dataForGraphs = calc.getAverages(time, key, location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators)
	if not dataForGraphs or False in dataForGraphs or [] in dataForGraphs:
		return False,0,0,0
	else:
		if sortOperators != 1:
			if weekly:
				a = 2
			else:
				a = 1
			averageDownlink = (sum([i[a] for i in dataForGraphs]) / len([i[a] for i in dataForGraphs]))	
			averageUplink = sum([i[a+1] for i in dataForGraphs]) / len([i[a+1] for i in dataForGraphs])
			averageLatency = sum([i[a+2] for i in dataForGraphs]) / len([i[a+2] for i in dataForGraphs])
		else:
			averageDownlink = []
			averageUplink = []
			averageLatency = []
			if weekly:
				a = 2
			else:
				a = 1
			for operator in dataForGraphs:
				if operator:
					averageDownlink.append(sum([i[a] for i in operator]) / len([i[a] for i in operator]))	
					averageUplink.append(sum([i[a+1] for i in operator]) / len([i[a+1] for i in operator]))
					averageLatency.append(sum([i[a+2] for i in operator]) / len([i[a+2] for i in operator]))
			
		if longTime:
			drawGraphLongTime(dataForGraphs,location,sortOperators,filename)
		elif weekly:
			drawGraphWeek(dataForGraphs, location, resolution, sortOperators,filename)
		else:
			drawGraphDay(dataForGraphs, location, resolution, sortOperators,filename)
		return  1,averageDownlink,averageUplink,averageLatency

if __name__ == '__main__':
	key = 0
	location = 0
	typeOfLocation = 2
	longTime = 0
	weekly = 0
	typeOfLocation = 1
	longTime = 1
	time = datetime.date(2016,6,13)
	weekly = 1
	fir = 0
	timeWindow = -180
	resolution = 1
	sortOperators = 1
	isWeekly = True
	key = 0
	if(sys.argv[9] == "0"):
		sortOperators = 0
	elif(sys.argv[9] != "1"):
		sortOperators = sys.argv[9]
	if(sys.argv[1] != "0"):
		key = sys.argv[1]
	if(sys.argv[2] != "0"):
		location = sys.argv[2]
	createWantedGraph(time, key, location, int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), sortOperators, sys.argv[10])
