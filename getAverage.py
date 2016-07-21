import mysql.connector as mariadb
from _datetime import date, datetime, timedelta
import datetime
#from drawgraph import drawGraph

def getFromDataBase(time, key, typeOfData, lengthOfTime, operator):
      
    try:
        #Create connection to database
        mariadb_connection = mariadb.connect(user='root', password='pythontesti', database='postcodes')
        cursor = mariadb_connection.cursor()
        
        if typeOfData == 0:      
            #Query for data data
            #Select data from certain time window and postal code
            if not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND postalcode LIKE %s", (time,lengthOfTime, time,key,))
            #Select data from certain time window, postal code and operator
            else:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND postalcode LIKE %s AND networkoperator = %s",(time,lengthOfTime,time,key,operator))

        if typeOfData == 1:
            #Query for data data
            #Select data from certain time window and city
            cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND county = %s", (time,lengthOfTime,time,key,))
        
        if typeOfData == 2:
            #Select data from certain time window and user id
            cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s",(time,lengthOfTime,time,key,))
            
        #More querys can be added here
        
        mariadb_connection.close()
        #return list including fetched data
        return list(cursor)

    except:
        print("Couldn't create database connection")
        return []

    
def getAverages(time, key, weekly, fir, typeOfData, timeWindow, resolution, sortOperators):
    #datetime.date object
    #key: code, city, uid...
    #weekly: true = week, false = day
    #fir: true/false
    
    #typeOfData gets its values as follows:
    # 0 = db query by postal code
    # 1 = db query by city name
    # 2 = db query by user id
    # more to be added
    
    #timeWindow: how many days of data is fetched (if fir=true, this doesn't matter)
    #resolution: when drawing the graphs, this tells how many hours are included into one average.
    #sortOperators: true/false, whether separation of operators is desired.
    
    #some data alteration needed if key is postal code
    if typeOfData == 0:
        key = key + "%"
    
    #time is altered to include the given day
    time = time + timedelta(days = 1)
    
    if sortOperators:
        data = getAveragesSortOperators(time, key, weekly, fir, typeOfData, timeWindow, resolution, sortOperators)
    elif fir:
        data = getAveragesWeekFir(time, key, typeOfData, timeWindow, resolution, sortOperators)
    elif weekly:
        data = calculateAveragesWeekly(time, key, typeOfData, timeWindow, resolution, sortOperators)
    else:
        data = calculateAveragesDaily(time, key, typeOfData, timeWindow, resolution, sortOperators)
    return data

def getAveragesSortOperators(time, key, weekly, fir, typeOfData, timeWindow, resolution, sortOperators):   
    
    allData = []
    for operator in ["Elisa","Sonera","DNA"]:
        if fir:
            data = getAveragesWeekFir(time, key, typeOfData, timeWindow, resolution, operator)
        elif weekly:
            data = calculateAveragesWeekly(time, key, typeOfData, timeWindow, resolution, operator)
        else:
            data = calculateAveragesDaily(time, key, typeOfData, timeWindow, resolution, operator)
        allData.append(data)
    return allData
    
def getAveragesWeekFir(time, key, typeOfData, timeWindow, resolution, sortOperators):
    #This function calculates weekly averages, and also takes into account the previous 3 weeks 
    #as a simple FIR filter.
    
    for i in range(1,5):
            
        data = getFromDataBase(time, key, typeOfData, timeWindow,sortOperators)
        newData = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
        
        if i == 1:
            values = calculateAveragesWeekly(newData, resolution)
            for line in values:
                line[2] = line[2] * 0.9
                line[3] = line[3] * 0.9
                line[4] = line[4] * 0.9
            
        elif i == 2:
            temp = calculateAveragesWeekly(newData, resolution)
            for line in range(len(temp)):
                values[line][2] += values[line][2] * 0.05
                values[line][3] += values[line][3] * 0.05
                values[line][4] += values[line][4] * 0.05
            
        elif i == 3:
            temp = calculateAveragesWeekly(newData, resolution)
            for line in range(len(temp)):
                values[line][2] += values[line][2] * 0.025
                values[line][3] += values[line][3] * 0.025
                values[line][4] += values[line][4] * 0.025
            
        elif i == 4:
            temp = calculateAveragesWeekly(newData, resolution)
            for line in range(len(temp)):
                values[line][2] += values[line][2] * 0.025
                values[line][3] += values[line][3] * 0.025
                values[line][4] += values[line][4] * 0.025
                
        time = time - timedelta(days = 7)
    return values

def calculateAveragesDaily(time,key,typeOfData,timeWindow,resolution,sortOperators):  
    
    data = getFromDataBase(time, key, typeOfData, timeWindow,sortOperators)
    data = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
    data.sort(key=lambda x: (x[0]))
    
    averages = []
    
    for hour in range(0,24):
        averages.append([hour,0,0,0,0])
        
    for line in data:
        indexInAverages = line[0].hour
        
        averages[indexInAverages][1] += line[3]
        averages[indexInAverages][2] += line[4]
        averages[indexInAverages][3] += line[2]
        averages[indexInAverages][4] += 1
               
    for valueSet in averages:
        if valueSet[4]:
            valueSet[1] = valueSet[1] / valueSet[4]
            valueSet[2] = valueSet[2] / valueSet[4]
            valueSet[3] = valueSet[3] / valueSet[4]
        
    if resolution > 1:
                 
        averagesNew = []
        
        for hour in range(0,24,resolution):
            counter = 0
            temp = [0, 0, 0, 0, 0]
            for valueSet in averages:
                if valueSet[0] >= hour and valueSet[0] < hour + resolution:
                    temp[0] = hour
                    temp[1] += valueSet[1]
                    temp[2] += valueSet[2]
                    temp[3] += valueSet[3]
                    temp[4] += valueSet[4]
                    if valueSet[4]:
                        counter += 1
            if temp[4]:
                temp[1] = temp[1]/counter
                temp[2] = temp[2]/counter
                temp[3] = temp[3]/counter
            averagesNew.append(temp)
        averages = averagesNew
        	
    averagesNoZeros = [i for i in averages if i[-1]]
    return averagesNoZeros

def calculateAveragesWeekly(time,key,typeOfData,timeWindow,resolution,sortOperators):  
    
    data = getFromDataBase(time, key,  typeOfData, timeWindow,sortOperators)
    data = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
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
    
    averagesNoZeros = [i for i in averages if i[-1]]
    return averagesNoZeros

if __name__ == '__main__':
    #time = datetime.date object
    time = datetime.date(2016,6,13)
    #key = postal code, city name, uid...
    key = "Espoo"
    #typeOfData as follows:
    # 0 = db query by postal code
    # 1 = db query by city name
    # 2 = db query by user id
    typeOfData = 1
    #from how many days datais acquired
    timeWindow = -7
    #averages are calculated for every [resolution] hours, values 1-24
    resolution = 1
    #use fir calculation or not, true/false
    fir = 0
    #sort by operators, true/false
    sortOperators = 0
    #weekly or daily averages, true=weekly/false=daily
    weekly = 1
    
    
    data = getAverages(time, key, weekly, fir, typeOfData, timeWindow, resolution, sortOperators)
    print(data)