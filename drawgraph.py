import matplotlib
import matplotlib.pyplot as plt
import pylab
import numpy as np

def drawGraphLongTime(data,location,sortOperators,filename):
	if sortOperators == 1:
		#First subplot: upload averages
		plt.subplot(211)
		maxAll = max([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		minAll = min([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		
		res = (maxAll - minAll) / 100

		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		

		plt.plot([i[0] for i in data[0]], [i[1] for i in data[0]], color = 'red')
		plt.plot([i[0] for i in data[1]], [i[1] for i in data[1]], color = 'green')
		plt.plot([i[0] for i in data[2]], [i[1] for i in data[2]], color = 'blue')
		plt.grid(True)
		
		temp = [i[0] for i in data[0]]
		plt.text(temp[3],maxAll- res*15, "Elisa", fontsize=14,color = 'red')
		plt.text(temp[20], maxAll - res*15, "DNA", fontsize=14, color = 'blue')
		plt.text(temp[37], maxAll - res*15, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		plt.title(location + ": " + "eri operaattorien keskiarvot" )
		plt.ylabel("Latausnopeus(kbps)")	
		
		#Second subplot: download averages
		plt.subplot(212)
		
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
		plt.ylabel("Lahetysnopeus(kbps)")	

	elif sortOperators in ["Elisa","Sonera","DNA"]:
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
		plt.text(temp[3], minAll + res, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll, maxAll)
		
		plt.title(sortOperators + "n verkon keskiarvot alueelta " + location )

	else:
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
		plt.text(temp[3], minAll + res, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll, maxAll)
		
		plt.title("Keskiarvot alueelta " + location )

	plt.gcf().autofmt_xdate()
	pylab.savefig(filename)

def drawGraphWeek(data, location, resolution, sortOperators,filename):
	days = ["MA", "TI", "KE", "TO", "PE", "LA", "SU"]
	if sortOperators == 1:
		#First subplot: upload averages
		x = [1/24 * i[1] + 1 + i[0] for i in data[0]]
		
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
		plt.ylabel("Latausnopeus(kbps)")	
		
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
		plt.ylabel("Lahetysnopeus(kbps)")	
		
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)
		
	elif sortOperators in ["Elisa", "DNA", "Sonera"]:
		x = [1/24 * i[1] + 1 + i[0] for i in data]
		y1 = [i[2] for i in data]
		y2 = [i[3] for i in data]
	
		averageY1 = sum(y1) / len(y1)
		averageY2 = sum(y2) / len(y2)
			
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
		plt.text(1, minAll+res, "Lahetysnopeus", fontsize=14, color = 'blue')
		
		plt.ylim(minAll, maxAll)
		
		plt.title(sortOperators + "n verkon viikottaiset keskiarvot alueelta " + location)
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)
		
	else:
		x = [1/24 * i[1] + 1 + i[0] for i in data]
		y1 = [i[2] for i in data]
		y2 = [i[3] for i in data]
	
		averageY1 = sum(y1) / len(y1)
		averageY2 = sum(y2) / len(y2)
		
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
		plt.text(1, minAll+res, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll,maxAll)
		
		plt.title("Viikottaiset keskiarvot alueelta " + location)
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)
	pylab.savefig(filename)

def drawGraphDay(data, location, resolution, sortOperators,filename):
	matplotlib.use('Agg')
	x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	if sortOperators == 1:
		#First subplot: upload averages
		plt.subplot(211)
		maxAll = max([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		minAll = min([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		res = (maxAll - minAll) / 100

		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
			
		plt.plot(x, [i[1] for i in data[0]], color = 'red')
		plt.plot(x, [i[1] for i in data[1]], color = 'green')
		plt.plot(x, [i[1] for i in data[2]], color = 'blue')
		plt.grid(True)
		
		plt.text(0.5,maxAll -res*15, "Elisa", fontsize=14,color = 'red')
		plt.text(4.5, maxAll - res*15, "DNA", fontsize=14, color = 'blue')
		plt.text(8.5, maxAll - res*15, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		plt.title(location + ": " + "eri operaattorien paivittaiset keskiarvot" )
		plt.ylabel("Latausnopeus(kbps)")	
		plt.xlim(0,23)
		
		#Second subplot: download averages
		plt.subplot(212)
		
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
		
		plt.text(0.5, maxAll -res*15, "Elisa", fontsize=14,color = 'red')
		plt.text(4.5, maxAll -res*15, "DNA", fontsize=14, color = 'blue')
		plt.text(8.5, maxAll -res*15, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		plt.xlim(0,23)
		plt.ylabel("Lahetysnopeus(kbps)")	
		
	elif sortOperators in ["Elisa", "DNA", "Sonera"]:
		y1 = [i[1] for i in data]
		y2 = [i[2] for i in data]
	
		averageY1 = sum(y1) / len(y1)
		averageY2 = sum(y2) / len(y2)
			
		plt.subplot(111)
		maxAll = max([i[1] for i in data]+[i[2] for i in data])
		minAll = min([i[1] for i in data]+[i[2] for i in data])
		res = (maxAll - minAll) / 100

		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		if maxAll * 0.08<2200:
			gap = 2200
		else:
			gap = maxAll * 0.08
		plt.plot(x, [i[1] for i in data], color = "red")
		plt.plot(x, [i[2] for i in data], color = "blue")
		plt.plot([0,23],[averageY1, averageY1], color = "red", linestyle = "--")
		plt.plot([0,23],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		plt.grid(True)

		plt.text(0.5, maxAll - gap, "Latausnopeus", fontsize=14, color='red')
		plt.text(0.5, minAll+res, "Lahetysnopeus", fontsize=14, color = 'blue')
		
		plt.ylim(minAll, maxAll)
		
		plt.title(sortOperators + "n verkon paivittaiset keskiarvot alueelta " + location)
		plt.xlim(0,23)
		
	else:
		y1 = [i[1] for i in data]
		y2 = [i[2] for i in data]
	
		averageY1 = sum(y1) / len(y1)
		averageY2 = sum(y2) / len(y2)
		
		plt.subplot(111)
		maxAll = max([i[1] for i in data]+[i[2] for i in data])
		minAll = min([i[1] for i in data]+[i[2] for i in data])
		res = (maxAll - minAll) / 100

		if minAll - res*10 < 0:
			minAll = 0
		else:
			minAll = minAll- res*10 
		maxAll = maxAll + res*20
		
		if maxAll * 0.08<2200:
			gap = 2200
		else:
			gap = maxAll * 0.08
		plt.plot(x, [i[1] for i in data], color = "red")
		plt.plot(x, [i[2] for i in data], color = "blue")
		plt.plot([0,23],[averageY1, averageY1], color = "red", linestyle = "--")
		plt.plot([0,23],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		plt.grid(True)
		
		plt.text(0.5, maxAll-gap, "Latausnopeus", fontsize=14, color='red')
		plt.text(0.5, minAll+res, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll, maxAll)
		if location:		
			plt.title("Paivittaisest keskiarvot alueelta " + location)
			
		plt.xlim(0,23)

	pylab.savefig(filename)
