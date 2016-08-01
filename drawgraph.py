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
		if minAll - 1000 < 0:
			minAll = 0
		else:
			minAll = minAll- 3000

		ax.plot([i[0] for i in data[0]], [i[1] for i in data[0]], color = 'red')
		ax.plot([i[0] for i in data[1]], [i[1] for i in data[1]], color = 'green')
		ax.plot([i[0] for i in data[2]], [i[1] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		temp = [i[0] for i in data[0]]
		ax.text(temp[3],maxAll + 5700, "Elisa", fontsize=14,color = 'red')
		ax.text(temp[3], maxAll + 3400, "DNA", fontsize=14, color = 'blue')
		ax.text(temp[3], maxAll + 1100, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll + 9000)
		ax.set_title(location + ": " + "eri operaattorien keskiarvot" )
		plt.ylabel("Latausnopeus(kbps)")	
		
		#Second subplot: download averages
		ax = fig1.add_subplot(212)
		
		maxAll = max([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		minAll = min([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		if minAll - 1000 < 0:
			minAll = 0
		else:
			minAll = minAll- 3000

		ax.plot([i[0] for i in data[0]], [i[2] for i in data[0]], color = 'red')
		ax.plot([i[0] for i in data[1]], [i[2] for i in data[1]], color = 'green')
		ax.plot([i[0] for i in data[2]], [i[2] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		temp = [i[0] for i in data[0]]
		ax.text(temp[3],maxAll + 6700, "Elisa", fontsize=14,color = 'red')
		ax.text(temp[3], maxAll + 4500, "DNA", fontsize=14, color = 'blue')
		ax.text(temp[3], maxAll + 2300, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll + 9000)
		plt.ylabel("Lahetysnopeus(kbps)")	

	elif sortOperators in ["Elisa","Sonera","DNA"]:
		ax = fig1.add_subplot(111)
		maxBoth = max([i[1] for i in data]+[i[2] for i in data])
		minBoth = min([i[1] for i in data]+[i[2] for i in data])
		if minBoth - 1000 < 0:
			minBoth = 0
		else:
			minBoth = minBoth- 3000
		
		ax.plot([i[0] for i in data], [i[1] for i in data], color = "red")
		ax.plot([i[0] for i in data], [i[2] for i in data], color = "blue")
		ax.grid(True)

		temp = [i[0] for i in data]
		ax.text(temp[3], maxBoth+6700, "Latausnopeus", fontsize=14, color='red')
		ax.text(temp[3], maxBoth+4500, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minBoth, maxBoth + 9000)
		
		ax.set_title(sortOperators + ": " + location )

	else:
		ax = fig1.add_subplot(111)
		maxBoth = max([i[1] for i in data]+[i[2] for i in data])
		minBoth = min([i[1] for i in data]+[i[2] for i in data])
		if minBoth - 1000 < 0:
			minBoth = 0
		else:
			minBoth = minBoth- 3000
			
		ax.plot([i[0] for i in data], [i[1] for i in data], color = "red")
		ax.plot([i[0] for i in data], [i[2] for i in data], color = "blue")
		ax.grid(True)
		
		temp = [i[0] for i in data]
		ax.text(temp[3], maxBoth+6700, "Latausnopeus", fontsize=14, color='red')
		ax.text(temp[3], maxBoth+4500, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minBoth, maxBoth + 9000)
		
		ax.set_title("Keskiarvot alueelta " + location )

	fig1.autofmt_xdate()
	plt.show()

def drawGraphWeek(data, location, resolution, sortOperators):
	fig1 = plt.figure()
	days = ["MA", "TI", "KE", "TO", "PE", "LA", "SU"]
	if sortOperators == 1:
		#First subplot: upload averages
		x = [1/24 * i[1] + 1 + i[0] for i in data[0]]
		
		ax = fig1.add_subplot(211)
		maxAll = max([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		minAll = min([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		if minAll - 1000 < 0:
			minAll = 0
		else:
			minAll = minAll- 3000

		ax.plot(x, [i[2] for i in data[0]], color = 'red')
		ax.plot(x, [i[2] for i in data[1]], color = 'green')
		ax.plot(x, [i[2] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		ax.text(1,maxAll + 5700, "Elisa", fontsize=14,color = 'red')
		ax.text(1, maxAll + 3400, "DNA", fontsize=14, color = 'blue')
		ax.text(1, maxAll + 1100, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll + 9000)
		ax.set_title(location + ": " + "eri operaattorien keskiarvot viikon aikana" )
		plt.ylabel("Latausnopeus(kbps)")	
		
		plt.xticks(range(1,8), days, rotation='vertical')
		plt.xlim(1,8)
		
		#Second subplot: download averages
		ax = fig1.add_subplot(212)
		
		maxAll = max([i[3] for i in data[0]]+[i[3] for i in data[1]]+[i[3] for i in data[2]])
		minAll = min([i[3] for i in data[0]]+[i[3] for i in data[1]]+[i[3] for i in data[2]])
		if minAll - 1000 < 0:
			minAll = 0
		else:
			minAll = minAll- 3000
		print(maxAll,minAll)
		ax.plot(x, [i[3] for i in data[0]], color = 'red')
		ax.plot(x, [i[3] for i in data[1]], color = 'green')
		ax.plot(x, [i[3] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		ax.text(1, maxAll + 6700, "Elisa", fontsize=14,color = 'red')
		ax.text(1, maxAll + 4500, "DNA", fontsize=14, color = 'blue')
		ax.text(1, maxAll + 2300, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll + 9000)
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
		maxBoth = max([i[2] for i in data]+[i[3] for i in data])
		minBoth = min([i[2] for i in data]+[i[3] for i in data])
		if minBoth - 1000 < 0:
			minBoth = 0
		else:
			minBoth = minBoth- 3000
		
		ax.plot(x, [i[2] for i in data], color = "red")
		ax.plot(x, [i[3] for i in data], color = "blue")
		ax.plot([1,8],[averageY1, averageY1], color = "red", linestyle = "--")
		ax.plot([1,8],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		ax.grid(True)

		ax.text(1, maxBoth+6700, "Latausnopeus", fontsize=14, color='red')
		ax.text(1, maxBoth+4500, "Lahetysnopeus", fontsize=14, color = 'blue')
		
		plt.ylim(minBoth, maxBoth + 9000)
		
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
		maxBoth = max([i[2] for i in data]+[i[3] for i in data])
		minBoth = min([i[2] for i in data]+[i[3] for i in data])
		if minBoth - 1000 < 0:
			minBoth = 0
		else:
			minBoth = minBoth- 3000
			
		ax.plot(x, [i[2] for i in data], color = "red")
		ax.plot(x, [i[3] for i in data], color = "blue")
		ax.plot([1,8],[averageY1, averageY1], color = "red", linestyle = "--")
		ax.plot([1,8],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		ax.grid(True)
		
		ax.text(1, maxBoth+6700, "Latausnopeus", fontsize=14, color='red')
		ax.text(1, maxBoth+4500, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minBoth, maxBoth + 9000)
		
		ax.set_title("Keskiarvot alueelta " + location +" viikon aikana")
		plt.xticks(range(1,8), days, rotation=45)
		plt.xlim(1,8)

	plt.show()


def drawGraphDay(data, location, resolution, sortOperators):
	
	fig1 = plt.figure()
	x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	if sortOperators == 1:
		#First subplot: upload averages
		ax = fig1.add_subplot(211)
		maxAll = max([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		minAll = min([i[1] for i in data[0]]+[i[1] for i in data[1]]+[i[1] for i in data[2]])
		if minAll - 1000 < 0:
			minAll = 0
		else:
			minAll = minAll- 3000

		ax.plot(x, [i[1] for i in data[0]], color = 'red')
		ax.plot(x, [i[1] for i in data[1]], color = 'green')
		ax.plot(x, [i[1] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		ax.text(0.5,maxAll + 5700, "Elisa", fontsize=14,color = 'red')
		ax.text(0.5, maxAll + 3400, "DNA", fontsize=14, color = 'blue')
		ax.text(0.5, maxAll + 1100, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll + 9000)
		ax.set_title(location + ": " + "eri operaattorien keskiarvot paivan aikana" )
		plt.ylabel("Latausnopeus(kbps)")	
		plt.xlim(0,23)
		
		#Second subplot: download averages
		ax = fig1.add_subplot(212)
		
		maxAll = max([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		minAll = min([i[2] for i in data[0]]+[i[2] for i in data[1]]+[i[2] for i in data[2]])
		if minAll - 1000 < 0:
			minAll = 0
		else:
			minAll = minAll- 3000
		print(maxAll,minAll)
		ax.plot(x, [i[2] for i in data[0]], color = 'red')
		ax.plot(x, [i[2] for i in data[1]], color = 'green')
		ax.plot(x, [i[2] for i in data[2]], color = 'blue')
		ax.grid(True)
		
		ax.text(0.5, maxAll + 6700, "Elisa", fontsize=14,color = 'red')
		ax.text(0.5, maxAll + 4500, "DNA", fontsize=14, color = 'blue')
		ax.text(0.5, maxAll + 2300, "Sonera", fontsize=14, color = 'green')
		
		plt.ylim(minAll, maxAll + 9000)
		plt.xlim(0,23)
		plt.ylabel("Lahetysnopeus(kbps)")	
		
	elif sortOperators in ["Elisa", "DNA", "Sonera"]:
		y1 = [i[1] for i in data]
		y2 = [i[2] for i in data]
	
		averageY1 = sum(y1) / len(y1)
		averageY2 = sum(y2) / len(y2)
			
		ax = fig1.add_subplot(111)
		maxBoth = max([i[1] for i in data]+[i[2] for i in data])
		minBoth = min([i[1] for i in data]+[i[2] for i in data])
		if minBoth - 1000 < 0:
			minBoth = 0
		else:
			minBoth = minBoth- 3000
		
		ax.plot(x, [i[1] for i in data], color = "red")
		ax.plot(x, [i[2] for i in data], color = "blue")
		ax.plot([0,23],[averageY1, averageY1], color = "red", linestyle = "--")
		ax.plot([0,23],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		ax.grid(True)

		ax.text(0.5, maxBoth+6700, "Latausnopeus", fontsize=14, color='red')
		ax.text(0.5, maxBoth+4500, "Lahetysnopeus", fontsize=14, color = 'blue')
		
		plt.ylim(minBoth, maxBoth + 9000)
		
		ax.set_title(sortOperators + "n verkon keskiarvot alueelta " + location + " paivan aikana")
		plt.xlim(0,23)
		
	else:
		y1 = [i[1] for i in data]
		y2 = [i[2] for i in data]
	
		averageY1 = sum(y1) / len(y1)
		averageY2 = sum(y2) / len(y2)
		
		ax = fig1.add_subplot(111)
		maxBoth = max([i[1] for i in data]+[i[2] for i in data])
		minBoth = min([i[1] for i in data]+[i[2] for i in data])
		if minBoth - 1000 < 0:
			minBoth = 0
		else:
			minBoth = minBoth- 3000
			
		ax.plot(x, [i[1] for i in data], color = "red")
		ax.plot(x, [i[2] for i in data], color = "blue")
		ax.plot([0,23],[averageY1, averageY1], color = "red", linestyle = "--")
		ax.plot([0,23],[averageY2, averageY2], color = "blue", linestyle = "--")
	
		ax.grid(True)
		
		ax.text(0.5, maxBoth+6700, "Latausnopeus", fontsize=14, color='red')
		ax.text(0.5, maxBoth+4500, "Lahetysnopeus", fontsize=14, color = 'blue')
		plt.ylim(minBoth, maxBoth + 9000)
		
		ax.set_title("Keskiarvot alueelta " + location + " paivan aikana")
		plt.xlim(0,23)

	plt.show()
