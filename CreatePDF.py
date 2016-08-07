from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from CreateGraph import createWantedGraph
import matplotlib.pyplot as plt
import datetime


def consumerReport(time, location, typeOfLocation):
	
	#Initializing the pdf
	c = canvas.Canvas("netradar_report.pdf")
	
	#Draw netradar logo and line below that
	c.drawImage("netradar_1.png", 97,775, width=100,height=30,mask=None) 
	c.line(97,770,492,770)
	
	#Writing the headline
	c.setFont("Times-Roman", 25)
	c.drawCentredString(297,730,"Raportti alueelta " + location)
	
	#Weekly averages in the area, no operator sorting.
	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time, 0, location, typeOfLocation, 0, 1, 0, -60, 1, 0,"foo.png")
	if fig:
		c.drawImage("foo.png", 80, 460, width = 450, height = 260, mask =None)
		c.setFont("Times-Roman", 16)
		
		#Creating the box to display the numbers
		c.rect(145,400,250,65)
		c.drawString(150, 450, "Keskiarvoja:")
		c.setFont("Courier", 13)
		c.drawString(150, 435, "Latausnopeus:   " + "{0:.2f}".format(averageDownlink) + "mbps")
		c.drawString(150, 420, "Lähetysnopeus:  " + "{0:.2f}".format(averageUplink) + "mbps")
		c.drawString(150, 405, "Latenssi:       " + "{0:.2f}".format(averagePing) + "ms")
	
	#Daily averages in the are, no operator sorting.
	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time, 0, location, typeOfLocation, 0, 0, 0, -60, 1, 0,"foo2.png")
	if fig:
		c.drawImage("foo2.png", 80, 130, width = 450, height = 260, mask = None)
		c.setFont("Times-Roman", 16)
		
		#The box for the numbers.
		c.rect(145,50,300,85)
		c.drawString(150, 120, "Keskiarvoja:")
		c.setFont("Courier", 13)
		c.drawString(150, 90, "Latausnopeus:   " + "{0:.2f}".format(averageDownlink) + "mbps")
		c.drawString(150, 75, "Lähetysnopeus:  " + "{0:.2f}".format(averageUplink) + "mbps")
		c.drawString(150, 60, "Latenssi:       " + "{0:.2f}".format(averagePing) + "ms")
	
	#New page
	c.showPage()
	#And the logos again
	c.drawImage("netradar_1.png", 97,775, width=100,height=30,mask=None) 
	c.line(97,770,492,770)
	
	#Longtime averages, with operators separated.
	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time, 0, location, typeOfLocation, 1, 0, 0, -30, 1, 1,"foo3.png")
	if fig:
		c.drawImage("foo3.png", 80, 460, width = 450, height = 280, mask = None)
	
	#Daily averages with operators separated.
	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time, 0, location, typeOfLocation, 0, 0, 0, -60, 1, 1,"foo4.png")
	if fig:
		c.drawImage("foo4.png", 80, 130, width = 450, height = 280, mask = None)
		c.setFont("Times-Roman", 16)
		c.rect(145,50,300,85)
		c.drawString(150, 120, "Operaattorien keskiarvot:")
		c.setFont("Courier", 13)
		c.drawString(150, 105, " ".ljust(10) + "Elisa".ljust(10) + "Sonera".ljust(10) + "DNA".ljust(10))
		c.drawString(150, 90, "Lataus".ljust(10) + ("{0:.2f}".format(averageDownlink[0])).ljust(10) + ("{0:.2f}".format(averageDownlink[1])).ljust(10) + ("{0:.2f}".format(averageDownlink[2])).ljust(10))
		c.drawString(150, 75, "Lähetys".ljust(10) + ("{0:.2f}".format(averageUplink[0])).ljust(10) + ("{0:.2f}".format(averageUplink[1])).ljust(10) + ("{0:.2f}".format(averageUplink[2])).ljust(10))
		c.drawString(150, 60, "Latenssi".ljust(10) + ("{0:.2f}".format(averagePing[0])).ljust(10) + ("{0:.2f}".format(averagePing[1])).ljust(10) + ("{0:.2f}".format(averagePing[2])).ljust(10))
		
	#Save the pdf.
	c.save()

def enterpriseReport(time, key):
	
	c = canvas.Canvas("netradar_report.pdf")
	c.drawImage("netradar_1.png", 97,775, width=100,height=30,mask=None) 
	
	c.line(97,770,492,770)
	c.setFont("Times-Roman", 25)
	c.drawCentredString(297,730,"Raportti avaimella " + location)
	
	#Weekly averages for the key.
	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time, key, 0, 0, 0, 1, 0, -60, 1, 0,"foo.png")
	if fig:
		c.drawImage("foo.png", 80, 460, width = 450, height = 260, mask =None)
		c.setFont("Times-Roman", 16)
		c.rect(145,400,250,65)
		c.drawString(150, 450, "Keskiarvoja:")
		c.setFont("Courier", 13)
		
		c.drawString(150, 435, "Latausnopeus:   " + "{0:.2f}".format(averageDownlink) + "mbps")
		c.drawString(150, 420, "Lähetysnopeus:  " + "{0:.2f}".format(averageUplink) + "mbps")
		c.drawString(150, 405, "Latenssi:       " + "{0:.2f}".format(averagePing) + "ms")
	
	#Daily averages for the key
	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time, key, 0, 0, 0, 0, 0, -60, 1, 0,"foo2.png")
	if fig:
		c.drawImage("foo2.png", 80, 130, width = 450, height = 260, mask = None)
		c.setFont("Times-Roman", 16)
		c.rect(145,50,300,85)
		c.drawString(150, 120, "Keskiarvoja:")
		c.setFont("Courier", 13)
		c.drawString(150, 90, "Latausnopeus:   " + "{0:.2f}".format(averageDownlink) + "mbps")
		c.drawString(150, 75, "Lähetysnopeus:  " + "{0:.2f}".format(averageUplink) + "mbps")
		c.drawString(150, 60, "Latenssi:       " + "{0:.2f}".format(averagePing) + "ms")
	
	#New page
	c.showPage()
	
	c.drawImage("netradar_1.png", 97,775, width=100,height=30,mask=None) 
	c.line(97,770,492,770)
	
	#Long time averages for the key
	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time,key, 0, 0, 1, 0, 0, -30, 1, 0,"foo3.png")
	if fig:
		c.drawImage("foo3.png", 80, 460, width = 450, height = 280, mask = None)
		
	c.save()

if __name__ == '__main__':
	location = "00200"
	typeOfLocation = 1
	time = datetime.date(2016,6,13)
	key = "111809239560095991352"
	#consumerReport(time, location,typeOfLocation)
	enterpriseReport(time, key)