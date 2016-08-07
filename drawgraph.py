import matplotlib
import matplotlib.pyplot as plt
import pylab
import numpy as np
import datetime

def drawGraphLongTime(data,key,location,sortOperators,filename):
	#This drawGraph is used if long time averages are plotted.
	#Takes the data in, and saves it as filename
	
	#Clear figure
	plt.clf()
	if sortOperators == 1:
		#This is used if operators are separated.
		
		#First subplot: download averages
		plt.subplot(211)
		
		#Min and max vaues for data are taken here.
		maxAll = max([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		minAll = min([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		
		#res is used to scale the window and place the texts.
		res = (maxAll - minAll) / 100
		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		#Data is plotted
		#Red = elisa, blue = dna, green = sonera
		plt.plot([i[0] for i in data[0]], [i[1] for i in data[0]], color = 'red')
		plt.plot([i[0] for i in data[1]], [i[1] for i in data[1]], color = 'green')
		plt.plot([i[0] for i in data[2]], [i[1] for i in data[2]], color = 'blue')
		plt.grid(True)
		
		#Legends are added to the plot.
		temp = [i[0] for i in data[0]]
		plt.text(temp[3],maxAll- res*15, "Elisa", fontsize=14,color = 'red')
		plt.text(temp[20], maxAll - res*15, "DNA", fontsize=14, color = 'blue')
		plt.text(temp[37], maxAll - res*15, "Sonera", fontsize=14, color = 'green')
		
		#y-axis limits are set
		plt.ylim(minAll, maxAll)
		#title and labels are added
		plt.title(location + ": " + "eri operaattorien keskiarvot" )
		plt.ylabel("Lätausnopeus(kbps)")	
		
		#Second subplot: upload averages
		plt.subplot(212)
		#Identical to the first subplot
		maxAll = max([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		minAll = min([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		
		res = (maxAll - minAll) / 100
		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		plt.plot([i[0] for i in data[0]], [i[2] for i in data[0]], color = 'red')
		plt.plot([i[0] for i in data[1]], [i[2] for i in data[1]], color = 'green')
		plt.plot([i[0] for i in data[2]], [i[2] for i in data[2]], color = 'blue')
		plt.grid(True)
		
		temp = [i[0] for i in data[0]]
		plt.text(temp[3],maxAll -res*15, "Elisa", fontsize=14,color = 'red')
		plt.text(temp[20], maxAll - res*15, "DNA", fontsize=14, color = 'blue')
		plt.text(temp[37], maxAll - res*15, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		plt.ylabel("Lähetysnopeus(kbps)")	

	elif sortOperators in ["Elisa","Sonera","DNA"]:
		#This is used if only one operator is drawn.
		plt.subplot(111)
		maxAll = max([i[1] for i in data]+[i[2] for i in data])
		minAll = min([i[1] for i in data]+[i[2] for i in data])
		
		res = (maxAll - minAll) / 100
		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		plt.plot([i[0] for i in data], [i[1] for i in data], color = "red")
		plt.plot([i[0] for i in data], [i[2] for i in data], color = "blue")
		plt.grid(True)

		temp = [i[0] for i in data]
		plt.text(temp[3], maxAll - res*15, "Latausnopeus", fontsize=14, color='red')
		plt.text(temp[3], minAll + res, "Lähetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll, maxAll)
		
		plt.title(sortOperators + "n verkon keskiarvot alueelta " + location )

	else:
		#And this is used if no operator sorting is used.
		plt.subplot(111)
		maxAll = max([i[1] for i in data]+[i[2] for i in data])
		minAll = min([i[1] for i in data]+[i[2] for i in data])
		
		res = (maxAll - minAll) / 100

		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		plt.plot([i[0] for i in data], [i[1] for i in data], color = "red")
		plt.plot([i[0] for i in data], [i[2] for i in data], color = "blue")
		plt.grid(True)
		
		temp = [i[0] for i in data]
		plt.text(temp[3], maxAll - res*15, "Latausnopeus", fontsize=14, color='red')
		plt.text(temp[3], minAll + res, "Lähetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll, maxAll)
		
		#Also possibility to use key or location.
		if key:
			plt.title("Keskiarvot avaimella " + key )
		elif location:
			plt.title("Keskiarvot alueelta " + location )
			
	#This is used to place the dates on x-axis properly.
	plt.gcf().autofmt_xdate(bottom=0.2, rotation=30, ha='right')
	#And finally save figure
	pylab.savefig(filename)

def drawGraphWeek(data, key, location, resolution, sortOperators,filename):
	#This drawGraph is used to plot weekly data.
	plt.clf()
	#Days are stored in a list for x-axis
	days = ["MA", "TI", "KE", "TO", "PE", "LA", "SU"]
	if sortOperators == 1:
		#Again, if operators are sorted this is used.
		
		#x-axis values are converted from (day,hour) format
		x = [1/24 * i[1] + 1 + i[0] for i in data[0]]
		
		#First subplot: upload averages
		plt.subplot(211)
		maxAll = max([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		minAll = min([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		res = (maxAll - minAll) / 100

		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		plt.plot(x, [i[2] for i in data[0]], color = 'red')
		plt.plot(x, [i[2] for i in data[1]], color = 'green')
		plt.plot(x, [i[2] for i in data[2]], color = 'blue')
		plt.grid(True)
		
		plt.text(1,maxAll -res*15, "Elisa", fontsize=14,color = 'red')
		plt.text(2, maxAll -res*15, "DNA", fontsize=14, color = 'blue')
		plt.text(3, maxAll -res*15, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		plt.title(location + ": " + "eri operaattorien viikottaiset keskiarvot" )
		plt.ylabel("Lätausnopeus(kbps)")	
		
		#x-axis is set to show the weekdays
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)
		
		#Second subplot: download averages
		plt.subplot(212)
		
		maxAll = max([i[3] for i in data[0]]+[i[3] for i in data[1]]+[i[3] for i in data[2]])
		minAll = min([i[3] for i in data[0]]+[i[3] for i in data[1]]+[i[3] for i in data[2]])
		res = (maxAll - minAll) / 100

		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		plt.plot(x, [i[3] for i in data[0]], color = 'red')
		plt.plot(x, [i[3] for i in data[1]], color = 'green')
		plt.plot(x, [i[3] for i in data[2]], color = 'blue')
		plt.grid(True)
		
		plt.text(1, maxAll -res*15, "Elisa", fontsize=14,color = 'red')
		plt.text(2, maxAll -res*15, "DNA", fontsize=14, color = 'blue')
		plt.text(3, maxAll -res*15, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		plt.ylabel("Lähetysnopeus(kbps)")	
		
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)
		
	elif sortOperators in ["Elisa", "DNA", "Sonera"]:
		#If only on eoperator is plotted:
		x = [1/24 * i[1] + 1 + i[0] for i in data]
		y1 = [i[2] for i in data]
		y2 = [i[3] for i in data]
	
		#Averages are calculated, zeros are left out.
		averageY1 = sum([i for i in y1 if i > 0]) / len([i for i in y1 if i > 0])
		averageY2 = sum([i for i in y2 if i > 0]) / len([i for i in y2 if i > 0])
			
		plt.subplot(111)
		maxAll = max([i[2] for i in data]+[i[3] for i in data])
		minAll = min([i[2] for i in data]+[i[3] for i in data])
		
		res = (maxAll - minAll) / 100
		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
			
		plt.plot(x, [i[2] for i in data], color = "red")
		plt.plot(x, [i[3] for i in data], color = "blue")
		#And here average lines are drawn, with dashed line.
		plt.plot([1,8],[averageY1, averageY1], color = "red", linestyle = "--")
		plt.plot([1,8],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		plt.grid(True)

		plt.text(1, maxAll-res*15, "Latausnopeus", fontsize=14, color='red')
		plt.text(1, minAll+res, "Lähetysnopeus", fontsize=14, color = 'blue')
		
		plt.ylim(minAll, maxAll)
		
		plt.title(sortOperators + "n verkon viikottaiset keskiarvot alueelta " + location)
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)
		
	else:
		x = [1/24 * i[1] + 1 + i[0] for i in data]
		y1 = [i[2] for i in data]
		y2 = [i[3] for i in data]
	
		averageY1 = sum([i for i in y1 if i > 0]) / len([i for i in y1 if i > 0])
		averageY2 = sum([i for i in y2 if i > 0]) / len([i for i in y2 if i > 0])
		
		plt.subplot(111)
		maxAll = max([i[2] for i in data]+[i[3] for i in data])
		minAll = min([i[2] for i in data]+[i[3] for i in data])
		
		res = (maxAll - minAll) / 100
		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		
		plt.plot(x, [i[2] for i in data], color = "red")
		plt.plot(x, [i[3] for i in data], color = "blue")
		plt.plot([1,8],[averageY1, averageY1], color = "red", linestyle = "--")
		plt.plot([1,8],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		plt.grid(True)
		
		plt.text(1, maxAll-res*15, "Latausnopeus", fontsize=14, color='red')
		plt.text(1, minAll+res, "Lähetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll,maxAll)
		if key:
			plt.title("Viikottaiset keskiarvot avaimella " + key)
		elif location:
			plt.title("Viikottaiset keskiarvot alueelta " + location)				
				
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)
	pylab.savefig(filename)

def drawGraphDay(data,key, location, resolution, sortOperators,filename):
	#This drawGraph is used to plot daily data
	#Works the same as the previous ones
	plt.clf()
	#hours for x-axis are initialized
	x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	if sortOperators == 1:
		#First subplot: upload averages
		plt.subplot(211)
		maxAll = max([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		minAll = min([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		
		average1 = sum([i[1] for i in data[0] if i[1]>0]) / len([i[1] for i in data[0] if i[1]>0])
		average2 = sum([i[1] for i in data[1] if i[1]>0]) / len([i[1] for i in data[1] if i[1]>0])
		average3 = sum([i[1] for i in data[2] if i[1]>0]) / len([i[1] for i in data[2] if i[1]>0])

		res = (maxAll - minAll) / 100
		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
			
		plt.plot(x, [i[1] for i in data[0]], color = 'red')
		plt.plot(x, [i[1] for i in data[1]], color = 'green')
		plt.plot(x, [i[1] for i in data[2]], color = 'blue')
		
		plt.plot([0,23],[average1, average1], color = "red", linestyle = "--")
		plt.plot([0,23],[average2, average2], color = "green", linestyle = "--")
		plt.plot([0,23],[average3, average3], color = "blue", linestyle = "--")
		
		plt.grid(True)
		
		plt.text(0.5,maxAll -res*15, "Elisa", fontsize=14,color = 'red')
		plt.text(4.5, maxAll - res*15, "DNA", fontsize=14, color = 'blue')
		plt.text(8.5, maxAll - res*15, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		plt.title(location + ": " + "eri operaattorien päivittäiset keskiarvot" )
		plt.ylabel("Latausnopeus(kbps)")	
		plt.xlim(0,23)
		
		#Second subplot: download averages
		plt.subplot(212)
		
		maxAll = max([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		minAll = min([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		
		average1 = sum([i[2] for i in data[0] if i[2]>0]) / len([i[2] for i in data[0] if i[2]>0])
		average2 = sum([i[2] for i in data[1] if i[2]>0]) / len([i[2] for i in data[1] if i[2]>0])
		average3 = sum([i[2] for i in data[2] if i[2]>0]) / len([i[2] for i in data[2] if i[2]>0])
		
		res = (maxAll - minAll) / 100
		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		plt.plot(x, [i[2] for i in data[0]], color = 'red')
		plt.plot(x, [i[2] for i in data[1]], color = 'green')
		plt.plot(x, [i[2] for i in data[2]], color = 'blue')
		plt.plot([0,23],[average1, average1], color = "red", linestyle = "--")
		plt.plot([0,23],[average2, average2], color = "green", linestyle = "--")
		plt.plot([0,23],[average3, average3], color = "blue", linestyle = "--")
		
		plt.grid(True)
		
		plt.text(0.5, maxAll -res*15, "Elisa", fontsize=14,color = 'red')
		plt.text(4.5, maxAll -res*15, "DNA", fontsize=14, color = 'blue')
		plt.text(8.5, maxAll -res*15, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		plt.xlim(0,23)
		plt.ylabel("Lähetysnopeus(kbps)")	
		
	elif sortOperators in ["Elisa", "DNA", "Sonera"]:
		y1 = [i[1] for i in data]
		y2 = [i[2] for i in data]
	
		averageY1 = sum([i for i in y1 if i > 0]) / len([i for i in y1 if i > 0])
		averageY2 = sum([i for i in y2 if i > 0]) / len([i for i in y2 if i > 0])
			
		plt.subplot(111)
		maxAll = max([i[1] for i in data]+[i[2] for i in data])
		minAll = min([i[1] for i in data]+[i[2] for i in data])
		res = (maxAll - minAll) / 100

		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
	
		plt.plot(x, [i[1] for i in data], color = "red")
		plt.plot(x, [i[2] for i in data], color = "blue")
		plt.plot([0,23],[averageY1, averageY1], color = "red", linestyle = "--")
		plt.plot([0,23],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		plt.grid(True)

		plt.text(0.5, maxAll - res*15, "Latausnopeus", fontsize=14, color='red')
		plt.text(0.5, minAll+res, "Lähetysnopeus", fontsize=14, color = 'blue')
		
		plt.ylim(minAll, maxAll)
		
		plt.title(sortOperators + "n verkon päivittäiset keskiarvot alueelta " + location)
		plt.xlim(0,23)
		
	else:
		y1 = [i[1] for i in data]
		y2 = [i[2] for i in data]
	
		averageY1 = sum([i for i in y1 if i > 0]) / len([i for i in y1 if i > 0])
		averageY2 = sum([i for i in y2 if i > 0]) / len([i for i in y2 if i > 0])
		
		plt.subplot(111)
		maxAll = max([i[1] for i in data]+[i[2] for i in data])
		minAll = min([i[1] for i in data]+[i[2] for i in data])
		
		res = (maxAll - minAll) / 100
		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		plt.plot(x, [i[1] for i in data], color = "red")
		plt.plot(x, [i[2] for i in data], color = "blue")
		plt.plot([0,23],[averageY1, averageY1], color = "red", linestyle = "--")
		plt.plot([0,23],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		plt.grid(True)
		
		plt.text(0.5, maxAll-res*15, "Latausnopeus", fontsize=14, color='red')
		plt.text(0.5, minAll+res, "Lähetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll, maxAll)
		if key:
			plt.title("Päivittäiset keskiarvot avaimella " + key)
		elif location:
			plt.title("Päivittäiset keskiarvot alueelta " + location)
		plt.xlim(0,23)

	pylab.savefig(filename)
