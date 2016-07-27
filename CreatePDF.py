from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def pdfTesti(postcode, averageDownlink, averageUplink, averagePing):
	c = canvas.Canvas("pdftestaus.pdf")
	c.drawImage("/home/joppe/Pictures/netradar.png", 97,775, width=100,height=30,mask=None) 
	c.line(97,770,492,770)
	c.setFont("Times-Roman", 25)
	c.drawCentredString(297,730,"Raportti postinumerosta: " + postcode)
	c.drawImage("/home/joppe/Pictures/figure_2.png", 100, 440, width = 410, height = 280, mask =None)
	c.setFont("Times-Roman", 18)
	c.rect(145,370,250,65)
	c.drawString(150, 420, "Keskiarvoisia tunnuslukuja:")
	c.setFont("Times-Roman", 15)
	c.drawString(165, 405, "\nLatausnopeus: " + str(averageDownlink) + "mbps")
	c.drawString(165, 390, "\nLähetysnopeus: " + str(averageUplink) + "mbps")
	c.drawString(165, 375, "\nLatenssi: " + str(averagePing) + "ms")
	c.drawImage("/home/joppe/Pictures/otaniemioperaattoreittain.png", 100, 80, width = 410, height = 280, mask = None)
	c.setFont("Times-Roman", 18)
	c.rect(145,10,250,65)
	c.drawString(150, 60, "Keskiarvoisia tunnuslukuja operaattoreittain:")
	c.setFont("Times-Roman", 15)
	c.drawString(165, 45, "\nLatausnopeus: " + str(averageDownlink) + "mbps")
	c.drawString(165, 30, "\nLähetysnopeus: " + str(averageUplink) + "mbps")
	c.drawString(165, 15, "\nLatenssi: " + str(averagePing) + "ms")
	c.save()


