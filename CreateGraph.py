import getAverage as calc
import datetime
from drawgraph import *

def createWantedGraph(key,location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators):
	time = datetime.date(2016,6,1)
	dataForGraphs = calc.getAverages(time, key, location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators)
	if longTime:
		drawGraphLongTime(dataForGraphs,location)
	elif sortOperators:
		drawGraphForOperators(dataForGraphs, location)
	elif weekly:
		drawGraphWeekCross(dataForGraphs, location, resolution)
	else:
		drawGraphDay(dataForGraphs, location)

if __name__ == '__main__':
	key = 0
	location = "Helsinki"
	typeOfLocation = 0
	longTime = 1
	weekly = 0
	fir = 0
	timeWindow = -10
	resolution = 1
	sortOperators = 1
	createWantedGraph(key, location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators)