import getAverage as calc
import datetime
from drawgraph import *

def createWantedGraph(key,location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators):
	time = datetime.date(2016,6,13)
	dataForGraphs = calc.getAverages(time, key, location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators)
	if longTime:
		drawGraphLongTime(dataForGraphs,location,sortOperators)
	elif weekly:
		drawGraphWeek(dataForGraphs, location, resolution, sortOperators)
	else:
		drawGraphDay(dataForGraphs, location, resolution, sortOperators)

if __name__ == '__main__':
	key = 0
	location = "Espoo"
	typeOfLocation = 2
	longTime = 0
	
	weekly = 0
	fir = 0
	timeWindow = -30
	resolution = 1
	sortOperators = "Sonera"
	createWantedGraph(key, location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators)