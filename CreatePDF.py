from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from CreateGraph import createWantedGraph
import matplotlib.pyplot as plt
import datetime
'''
key = 0
location = "Helsinki"
typeOfLocation = 2
longTime = 0

weekly = 0
fir = 0
timeWindow = -30
resolution = 1
sortOperators = 1
'''
location = "00200"
typeOfLocation = 1
time = datetime.date(2016,6,6)

def consumerReport(time, location, typeOfLocation):
	
	c = canvas.Canvas("pdftestaus.pdf")
	c.drawImage("netradar_1.png", 97,775, width=100,height=30,mask=None) 
	
	c.line(97,770,492,770)
	c.setFont("Times-Roman", 25)
	c.drawCentredString(297,730,"Raportti alueelta " + location)

	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time, 0, location, typeOfLocation, 0, 1, 0, -60, 1, 0,"foo.png")
	if fig:
		c.drawImage("foo.png", 80, 460, width = 450, height = 260, mask =None)
		c.setFont("Times-Roman", 16)
		c.rect(145,400,250,65)
		c.drawString(150, 450, "Keskiarvoja:")
		c.setFont("Courier", 13)
		
		c.drawString(150, 435, "Latausnopeus:   " + "{0:.2f}".format(averageDownlink) + "mbps")
		c.drawString(150, 420, "Lähetysnopeus:  " + "{0:.2f}".format(averageUplink) + "mbps")
		c.drawString(150, 405, "Latenssi:       " + "{0:.2f}".format(averagePing) + "ms")
	
	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time, 0, location, typeOfLocation, 0, 0, 0, -60, 1, 0,"foo2.png")
	if fig:
		c.drawImage("foo2.png", 80, 130, width = 450, height = 260, mask = None)
		c.setFont("Times-Roman", 16)
		c.rect(145,50,300,85)
		c.drawString(150, 120, "Keskiarvoja:")
		c.setFont("Courier", 13)
		c.drawString(150, 90, "Latausnopeus:   " + "{0:.2f}".format(averageDownlink) + "mbps")
		c.drawString(150, 75, "Lähetysnopeus:  " + "{0:.2f}".format(averageUplink) + "mbps")
		c.drawString(150, 60, "Latenssi:       " + "{0:.2f}".format(averagePing) + "ms")
	
	
	c.showPage()
	
	c.drawImage("netradar_1.png", 97,775, width=100,height=30,mask=None) 
	
	c.line(97,770,492,770)
	
	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time, 0, location, typeOfLocation, 1, 0, 0, -30, 1, 1,"foo3.png")
	if fig:
		c.drawImage("foo3.png", 80, 460, width = 450, height = 280, mask = None)
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

	c.save()

def enterpriseReport(time, key):
	
	c = canvas.Canvas("pdftestaus.pdf")
	c.drawImage("netradar_1.png", 97,775, width=100,height=30,mask=None) 
	
	c.line(97,770,492,770)
	c.setFont("Times-Roman", 25)
	c.drawCentredString(297,730,"Raportti avaimella " + location)

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
	
	
	c.showPage()
	
	c.drawImage("netradar_1.png", 97,775, width=100,height=30,mask=None) 
	
	c.line(97,770,492,770)
	fig,averageDownlink,averageUplink,averagePing = createWantedGraph(time,key, 0, 0, 1, 0, 0, -30, 1, 0,"foo3.png")
	if fig:
		c.drawImage("foo3.png", 80, 460, width = 450, height = 280, mask = None)
		
	'''
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
	'''
	c.save()

if __name__ == '__main__':
	time = datetime.date(2016,6,13)
	key = "111809239560095991352"
	enterpriseReport(time, key)