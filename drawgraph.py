import matplotlib.pyplot as plt
import pylab
import numpy as np

def drawGraphLongTime(data,location,sortOperators):
	fig1 = plt.figure()
	if sortOperators == 1:
		#First subplot: upload averages
		ax = fig1.add_subplot(211)
		maxAll = max([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		minAll = min([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		
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

		ax.plot([i[0] for i in data[0]], [i[1] for i in data[0]], color = 'red')
		ax.plot([i[0] for i in data[1]], [i[1] for i in data[1]], color = 'green')
		ax.plot([i[0] for i in data[2]], [i[1] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		temp = [i[0] for i in data[0]]
		ax.text(temp[3],maxAll- gap, "Elisa", fontsize=14,color = 'red')
		ax.text(temp[20], maxAll - gap, "DNA", fontsize=14, color = 'blue')
		ax.text(temp[37], maxAll - gap, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		ax.set_title(location + ": " + "eri operaattorien keskiarvot" )
		plt.ylabel("Latausnopeus(kbps)")	
		
		#Second subplot: download averages
		ax = fig1.add_subplot(212)
		
		maxAll = max([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		minAll = min([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
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
		
		ax.plot([i[0] for i in data[0]], [i[2] for i in data[0]], color = 'red')
		ax.plot([i[0] for i in data[1]], [i[2] for i in data[1]], color = 'green')
		ax.plot([i[0] for i in data[2]], [i[2] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		temp = [i[0] for i in data[0]]
		ax.text(temp[3],maxAll -gap, "Elisa", fontsize=14,color = 'red')
		ax.text(temp[20], maxAll - gap, "DNA", fontsize=14, color = 'blue')
		ax.text(temp[37], maxAll - gap, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		plt.ylabel("Lahetysnopeus(kbps)")	

	elif sortOperators in ["Elisa","Sonera","DNA"]:
		ax = fig1.add_subplot(111)
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
			
		ax.plot([i[0] for i in data], [i[1] for i in data], color = "red")
		ax.plot([i[0] for i in data], [i[2] for i in data], color = "blue")
		ax.grid(True)

		temp = [i[0] for i in data]
		ax.text(temp[3], maxAll - gap, "Latausnopeus", fontsize=14, color='red')
		ax.text(temp[3], minAll + res, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll, maxAll)
		
		ax.set_title(sortOperators + ": " + location )

	else:
		ax = fig1.add_subplot(111)
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
				
		ax.plot([i[0] for i in data], [i[1] for i in data], color = "red")
		ax.plot([i[0] for i in data], [i[2] for i in data], color = "blue")
		ax.grid(True)
		
		temp = [i[0] for i in data]
		ax.text(temp[3], maxAll - gap, "Latausnopeus", fontsize=14, color='red')
		ax.text(temp[3], minAll + res, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll, maxAll)
		
		ax.set_title("Keskiarvot alueelta " + location )

	fig1.autofmt_xdate()
	#plt.show()
	pylab.savefig("testi.png")

def drawGraphWeek(data, location, resolution, sortOperators):
	fig1 = plt.figure()
	days = ["MA", "TI", "KE", "TO", "PE", "LA", "SU"]
	if sortOperators == 1:
		#First subplot: upload averages
		x = [1/24 * i[1] + 1 + i[0] for i in data[0]]
		
		ax = fig1.add_subplot(211)
		maxAll = max([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		minAll = min([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
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
			
		ax.plot(x, [i[2] for i in data[0]], color = 'red')
		ax.plot(x, [i[2] for i in data[1]], color = 'green')
		ax.plot(x, [i[2] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		ax.text(1,maxAll -gap, "Elisa", fontsize=14,color = 'red')
		ax.text(2, maxAll -gap, "DNA", fontsize=14, color = 'blue')
		ax.text(3, maxAll -gap, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		ax.set_title(location + ": " + "eri operaattorien keskiarvot viikon aikana" )
		plt.ylabel("Latausnopeus(kbps)")	
		
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)
		
		#Second subplot: download averages
		ax = fig1.add_subplot(212)
		
		maxAll = max([i[3] for i in data[0]]+[i[3] for i in data[1]]+[i[3] for i in data[2]])
		minAll = min([i[3] for i in data[0]]+[i[3] for i in data[1]]+[i[3] for i in data[2]])
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
			
		ax.plot(x, [i[3] for i in data[0]], color = 'red')
		ax.plot(x, [i[3] for i in data[1]], color = 'green')
		ax.plot(x, [i[3] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		ax.text(1, maxAll -gap, "Elisa", fontsize=14,color = 'red')
		ax.text(2, maxAll -gap, "DNA", fontsize=14, color = 'blue')
		ax.text(3, maxAll -gap, "Sonera", fontsize=14, color = 'green')
		
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
			
		ax = fig1.add_subplot(111)
		maxAll = max([i[2] for i in data]+[i[3] for i in data])
		minAll = min([i[2] for i in data]+[i[3] for i in data])
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
			
		ax.plot(x, [i[2] for i in data], color = "red")
		ax.plot(x, [i[3] for i in data], color = "blue")
		ax.plot([1,8],[averageY1, averageY1], color = "red", linestyle = "--")
		ax.plot([1,8],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		ax.grid(True)

		ax.text(1, maxAll-gap, "Latausnopeus", fontsize=14, color='red')
		ax.text(1, minAll+res, "Lahetysnopeus", fontsize=14, color = 'blue')
		
		plt.ylim(minAll, maxAll)
		
		ax.set_title(sortOperators + "n verkon keskiarvot alueelta " + location + " viikon aikana")
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)
		
	else:
		x = [1/24 * i[1] + 1 + i[0] for i in data]
		y1 = [i[2] for i in data]
		y2 = [i[3] for i in data]
	
		averageY1 = sum(y1) / len(y1)
		averageY2 = sum(y2) / len(y2)
		
		ax = fig1.add_subplot(111)
		maxAll = max([i[2] for i in data]+[i[3] for i in data])
		minAll = min([i[2] for i in data]+[i[3] for i in data])
		
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
			
		ax.plot(x, [i[2] for i in data], color = "red")
		ax.plot(x, [i[3] for i in data], color = "blue")
		ax.plot([1,8],[averageY1, averageY1], color = "red", linestyle = "--")
		ax.plot([1,8],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		ax.grid(True)
		
		ax.text(1, maxAll-gap, "Latausnopeus", fontsize=14, color='red')
		ax.text(1, minAll+res, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll,maxAll)
		
		ax.set_title("Keskiarvot alueelta " + location +" viikon aikana")
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)

	#plt.show()
	pylab.savefig("testi.png")

def drawGraphDay(data, location, resolution, sortOperators):
	
	fig1 = plt.figure()
	x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	if sortOperators == 1:
		#First subplot: upload averages
		ax = fig1.add_subplot(211)
		maxAll = max([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		minAll = min([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
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
			
		ax.plot(x, [i[1] for i in data[0]], color = 'red')
		ax.plot(x, [i[1] for i in data[1]], color = 'green')
		ax.plot(x, [i[1] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		ax.text(0.5,maxAll - gap, "Elisa", fontsize=14,color = 'red')
		ax.text(4.5, maxAll - gap, "DNA", fontsize=14, color = 'blue')
		ax.text(8.5, maxAll - gap, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		ax.set_title(location + ": " + "eri operaattorien keskiarvot paivan aikana" )
		plt.ylabel("Latausnopeus(kbps)")	
		plt.xlim(0,23)
		
		#Second subplot: download averages
		ax = fig1.add_subplot(212)
		
		maxAll = max([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		minAll = min([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
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
		ax.plot(x, [i[2] for i in data[0]], color = 'red')
		ax.plot(x, [i[2] for i in data[1]], color = 'green')
		ax.plot(x, [i[2] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		ax.text(0.5, maxAll -gap, "Elisa", fontsize=14,color = 'red')
		ax.text(4.5, maxAll -gap, "DNA", fontsize=14, color = 'blue')
		ax.text(8.5, maxAll -gap, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll)
		plt.xlim(0,23)
		plt.ylabel("Lahetysnopeus(kbps)")	
		
	elif sortOperators in ["Elisa", "DNA", "Sonera"]:
		y1 = [i[1] for i in data]
		y2 = [i[2] for i in data]
	
		averageY1 = sum(y1) / len(y1)
		averageY2 = sum(y2) / len(y2)
			
		ax = fig1.add_subplot(111)
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
		ax.plot(x, [i[1] for i in data], color = "red")
		ax.plot(x, [i[2] for i in data], color = "blue")
		ax.plot([0,23],[averageY1, averageY1], color = "red", linestyle = "--")
		ax.plot([0,23],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		ax.grid(True)

		ax.text(0.5, maxAll - gap, "Latausnopeus", fontsize=14, color='red')
		ax.text(0.5, minAll+res, "Lahetysnopeus", fontsize=14, color = 'blue')
		
		plt.ylim(minAll, maxAll)
		
		ax.set_title(sortOperators + "n verkon keskiarvot alueelta " + location + " paivan aikana")
		plt.xlim(0,23)
		
	else:
		y1 = [i[1] for i in data]
		y2 = [i[2] for i in data]
	
		averageY1 = sum(y1) / len(y1)
		averageY2 = sum(y2) / len(y2)
		
		ax = fig1.add_subplot(111)
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
		ax.plot(x, [i[1] for i in data], color = "red")
		ax.plot(x, [i[2] for i in data], color = "blue")
		ax.plot([0,23],[averageY1, averageY1], color = "red", linestyle = "--")
		ax.plot([0,23],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		ax.grid(True)
		
		ax.text(0.5, maxAll-gap, "Latausnopeus", fontsize=14, color='red')
		ax.text(0.5, minAll+res, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minAll, maxAll)
		
		ax.set_title("Keskiarvot alueelta " + location + " paivan aikana")
		plt.xlim(0,23)

	#plt.show()
	pylab.savefig("testi.png")

