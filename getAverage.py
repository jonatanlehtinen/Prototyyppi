

@author: Lare

import matplotlib.pyplot as plt
=======

import mysql.connector as mariadb
from _datetime import date, datetime
import datetime

'''
def getFromDataBase(time, code, typeOfData, lengthOfTime):
     

	if typeOfData == 0:
		#try:
		#Create connection to database
		mariadb_connection = mariadb.connect(user='root', password='pythontesti', database='Otaniemi')
		cursor = mariadb_connection.cursor()
		
		#Query for right data
		cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND postalcode LIKE %s AND radiotype='cell'", (time,lengthOfTime, time,code,))
		mariadb_connection.close()
		
		#return list including fetched data
		return list(cursor)
		#except:
		#    print("Couldn't create database connection")
		#    return []
'''   
	if typeOfData == 1:

    if typeOfData == 0:
        try:
        #Create connection to database
            mariadb_connection = mariadb.connect(user='root', password='pythontesti', database='postcodes')
            cursor = mariadb_connection.cursor()
            
            #Query for right data
            cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode FROM otaniemidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND postalcode LIKE %s AND radiotype='cell'", (time,lengthOfTime, time,code,))
            mariadb_connection.close()
            
            #return list including fetched data
            return list(cursor)
        except:
            print("Couldn't create database connection")
            return []
   
    if typeOfData == 1:
        try:
            #Create connection to database
            mariadb_connection = mariadb.connect(user='root', password='pythontesti', database='Otaniemi')
            cursor = mariadb_connection.cursor()
            
            #Query for right data
            cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode FROM otaniemitesti3 WHERE DATEDIFF(%s,startedAt)<%s AND uid LIKE %s", (time,lengthOfTime,code,))

            cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode FROM otaniemidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid LIKE %s", (time,lengthOfTime,code,))

            mariadb_connection.close()
            
            #return list including fetched data
            return list(cursor)
        except:
            print("Couldn't create database connection")
            return []

    
def getAverages():
    time = datetime.date(2016,6,13)
    code = "02150%"
    #typeOfData is used to store whether the user wants postal code, user id or something else.
    typeOfData = 0
    lengthOfTime = -150
    data = getFromDataBase(time, code, typeOfData, lengthOfTime)
    #.strftime("%Y-%m-%d %H:%M:%S")
    newData = [(item[0], item[1], item[2], item[3], item[4], item[5][:5]) for item in data]

    averages = calculateAverages(newData)
    print(averages)
    return averages
    
def calculateAverages(newData):  
	data = [(item[0].hour, item[1], item[2], item[3], item[4], item[5][:5]) for item in newData]
	data.sort(key=lambda x: (x[0]))

	averages = []
	for hour in range(0,25):
		counter = 0
		for line in data:
			if not averages and line[0] == hour:
				averages.append([])
				averages[-1].append(hour)
				averages[-1].append(line[3])
				averages[-1].append(line[4])
				averages[-1].append(line[2])

			elif line[0] == hour and hour not in [i[0] for i in averages]:
				averages.append([])
				averages[-1].append(hour)
				averages[-1].append(line[3])
				averages[-1].append(line[4])
				averages[-1].append(line[2])
				counter += 1
			elif line[0] == hour:
				averages[-1][1] += line[3]
				averages[-1][2] += line[4]
				averages[-1][3] += line[2]
				counter += 1
		if counter:
			averages[-1][1] = averages[-1][1] / counter
			averages[-1][2] = averages[-1][2] / counter
			averages[-1][3] = averages[-1][3] / counter
			averages[-1].append(counter)
	return averages
  

def drawGraph():  
	data = getAverages()
	print(data)
	x1 = [i[0] for i in data]
	y1 = [i[1] for i in data]
	y2 = [i[2] for i in data]

	maxY = max(y1+y2)
	minY = min(y1+y2)
	minX = min(x1)

	y3 = [i[3] for i in data]
	
	fig2 = plt.figure()
	ax1 = fig2.add_subplot(111)
	ax1.plot(x1, y3)	

	fig1 = plt.figure()
	ax = fig1.add_subplot(111)
	ax.plot(x1,y1, color = "red", marker = "o")
	ax.plot(x1,y2, color = "blue", marker = "o")
	ax.grid(True)
	plt.ylim(max(0,minY - 7000),maxY + 7000)
	plt.xlim(0, 23)
	ax.set_title("Otaniemen data 2016")
	ax.text(int(minX+1), int(maxY+4000), "Red plot: download", fontsize=13)
	ax.text(int(minX+1), int(maxY), "Blue plot: upload", fontsize=13)
	plt.xlabel("Time")
	plt.ylabel("Speed(kbps)")
	plt.show()


'''
def keskiarvo(values,conn_type):
    
    averages = []
    
    if conn_type:
        for line in range(len(values)):
            
            temp_str = values[line][0]+ ","+  values[line][2]
            
            if temp_str not in [i[0] for i in averages]:   
                
                averages.append([])
                averages[-1].append(temp_str)
                averages[-1].append(float(values[line][1]))
                averages[-1].append(1)
                
            else:       
                temp = [i[0] for i in averages].index(temp_str)  
                
                averages[temp][1] += float(values[line][1])
                averages[temp][2] += 1
     
    else:
        for line in range(len(values)):
            
            temp_str = values[line][0]
            
            if temp_str not in [i[0] for i in averages]:   
                
                averages.append([])
                averages[-1].append(temp_str)
                averages[-1].append(float(values[line][1]))
                averages[-1].append(1)
                
            else:       
                temp = [i[0] for i in averages].index(temp_str)  
                
                averages[temp][1] += float(values[line][1])
                averages[temp][2] += 1
      
    for line in range(len(averages)):
       
        averages[line][1] = averages[line][1] / averages[line][2]
    
    return averages   
'''
if __name__ == '__main__':
        getAverages()    
