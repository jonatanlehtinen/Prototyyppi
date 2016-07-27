import calculateAverage as calc
from drawgraph import *

def createWantedGraph(key,location, typeOfLocation, weekly, fir, timeWindow, resolution, sortOperators):
	time = datetime.date(2016,6,13)
	dataForGraphs = calc.getAverages(time, key, location, typeOfLocation, weekly, fir, timeWindow, resolution, sortOperators)
	
	if sortOperators:
		drawGraphForOperators(dataForGraphs, location)
	elif weekly:
		drawGraphWeekCross(dataForGraphs, location, resolution)
	else:
		drawGraphDay(dataForGraphs, location)
