import mysql.connector as mariadb
from _datetime import date, datetime
import datetime
#from drawgraph import drawGraph


def getFromDataBase(time, code, typeOfData, lengthOfTime):

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
    resolution = 2
    lengthOfTime = -150
    data = getFromDataBase(time, code, typeOfData, lengthOfTime)
    #.strftime("%Y-%m-%d %H:%M:%S")
    newData = [(item[0], item[1], item[2], item[3], item[4], item[5][:5]) for item in data]
    averages = calculateAveragesWeek(newData,resolution)
    print(averages)
    
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
  
def calculateAveragesWeek(newData,resolution):  
    data = [(item[0], item[1], item[2], item[3], item[4], item[5][:5]) for item in newData]
    data.sort(key=lambda x: (x[0]))

    averages = []
    for day in range(0,7):
        for hour in range(0,24):
            averages.append([day,hour,0,0,0,0])
            
    for line in data:
        indexInAverages = line[0].weekday()*24 + line[0].hour
        
        averages[indexInAverages][2] += line[3]
        averages[indexInAverages][3] += line[4]
        averages[indexInAverages][4] += line[2]
        averages[indexInAverages][5] += 1
               
    for valueSet in averages:
        if valueSet[5]:
            valueSet[2] = valueSet[2] / valueSet[5]
            valueSet[3] = valueSet[3] / valueSet[5]
            valueSet[4] = valueSet[4] / valueSet[5]
    
    if resolution > 1:
                 
        averagesNew = []
        for day in range(0,7):
            for hour in range(0,24,resolution):
                counter = 0
                temp = [0, 0, 0, 0, 0, 0]
                for valueSet in averages:
                    if valueSet[0] == day and valueSet[1] >= hour and valueSet[1] < hour + resolution:
                        temp[0] = day
                        temp[1] = hour
                        temp[2] += valueSet[2]
                        temp[3] += valueSet[3]
                        temp[4] += valueSet[4]
                        temp[5] += valueSet[5]
                        if valueSet[5]:
                            counter += 1
                if temp[5]:
                    temp[2] = temp[2]/counter
                    temp[3] = temp[3]/counter
                    temp[4] = temp[4]/counter
                    averagesNew.append(temp)
        averages = averagesNew
    return averages

if __name__ == '__main__':
        getAverages()    
