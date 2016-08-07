import getAverage as calc
import datetime
from drawgraph import *
import sys

def createWantedGraph(time, key,location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators,filename):
	#This function is given the parameters, then calls the getAverages and then gives
	#those averages to the drawGraph.
	dataForGraphs = calc.getAverages(time, key, location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators)
	if not dataForGraphs or False in dataForGraphs or [] in dataForGraphs:
		return False,0,0,0
	else:
		#Some averages are calculated
		if sortOperators != 1:
			#a is set accroding to weekly/daily, because the format differs.
			if weekly:
				a = 2
			else:
				a = 1
			averageDownlink = sum([i[a] for i in dataForGraphs if i[a] > 0]) / len([i[a] for i in dataForGraphs if i[a]>0])	
			averageUplink = sum([i[a+1] for i in dataForGraphs if i[a+1]>0]) / len([i[a+1] for i in dataForGraphs if i[a+1]>0])
			averageLatency = sum([i[a+2] for i in dataForGraphs if i[a+2]>0]) / len([i[a+2] for i in dataForGraphs if i[a+2]>0])
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
					averageDownlink.append(sum([i[a] for i in operator if i[a]>0]) / len([i[a] for i in operator if i[a]>0]))	
					averageUplink.append(sum([i[a+1] for i in operator if i[a+1]>0]) / len([i[a+1] for i in operator if i[a+1]>0]))
					averageLatency.append(sum([i[a+2] for i in operator if i[a+2]>0]) / len([i[a+2] for i in operator if i[a+2]>0]))
		#DrawGraphs are called.	
		if longTime:
			drawGraphLongTime(dataForGraphs,key,location,sortOperators,filename)
		elif weekly:
			drawGraphWeek(dataForGraphs,key, location, resolution, sortOperators,filename)
		else:
			drawGraphDay(dataForGraphs,key, location, resolution, sortOperators,filename)
		#if called by createPDF, these are returned
		return  1,averageDownlink,averageUplink,averageLatency

if __name__ == '__main__':
	key = "111809239560095991352" 
	location = 0
	typeOfLocation = 0
	longTime = 0
	time = datetime.date(2016,6,13)
	weekly = 0
	fir = 0
	timeWindow = -60
	resolution = 1
	sortOperators = 0
	isWeekly = True
	key = 0
	if(sys.argv[9] == "0"):
		sortOperators = 0
	elif(sys.argv[9] == "1"):
		sortOperators = 1
	else:
		sortOperators = sys.argv[9]
	if(sys.argv[1] != "0"):
		key = sys.argv[1]
	if(sys.argv[2] != "0"):
		location = sys.argv[2]
	createWantedGraph(time, key, location, int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), sortOperators, sys.argv[10])
