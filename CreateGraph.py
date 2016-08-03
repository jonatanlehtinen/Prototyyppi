import getAverage as calc
import datetime
from drawgraph import *

def createWantedGraph(time, key,location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators,filename):
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
	location = "02100"
	typeOfLocation = 1
	longTime = 1
	time = datetime.date(2016,6,6)
	weekly = 1
	fir = 0
	timeWindow = -180
	resolution = 1
	sortOperators = 1
	filename = "bar.png"
	createWantedGraph(time, key, location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators,filename)