import mysql.connector as mariadb
from _datetime import date, datetime, timedelta
import datetime
from drawgraph import drawGraph

def getFromDataBase(time, key, location, typeOfLocation, lengthOfTime, operator):
      
    try:
        #Create connection to database
        mariadb_connection = mariadb.connect(user='root', password='pythontesti', database='postcodes')
        cursor = mariadb_connection.cursor()
        
        if typeOfLocation == 0:      
            #Query for data 
            #Select data from certain time window and possibly key
            if not key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s", (time,lengthOfTime, time,))
            elif key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s",(time,lengthOfTime,time,key,))
            elif not key and operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND networkoperator = %s",(time,lengthOfTime,time,operator,))
            else:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s AND networkoperator = %s",(time,lengthOfTime,time,key,operator))

        if typeOfLocation == 1:
            #Query for data 
            #Select data from certain time window and postal code
            if not key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND postalcode LIKE %s", (time,lengthOfTime, time,location,))
            elif key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s AND postalcode LIKE %s",(time,lengthOfTime,time,key,location,))
            elif not key and operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND networkoperator = %s AND postalcode LIKE %s",(time,lengthOfTime,time,operator,location))
            else:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s AND networkoperator = %s AND postalcode LIKE %s",(time,lengthOfTime,time,key,operator,location))

        if typeOfLocation == 2:
            #Select data from certain time window and city
            if not key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND county = %s", (time,lengthOfTime, time,location,))
            elif key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s AND county = %s",(time,lengthOfTime,time,key,location,))
            elif not key and operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND networkoperator = %s AND county = %s",(time,lengthOfTime,time,operator,location))
            else:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM otaniemitesti3 WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s AND networkoperator = %s AND county = %s",(time,lengthOfTime,time,key,operator,location))
            
        #More querys can be added here
        
        mariadb_connection.close()
        #return list including fetched data
        return list(cursor)

    except:
        print("Couldn't create database connection")
        return []

    
def getAverages(time, key, location, typeOfLocation, weekly, fir, timeWindow, resolution, sortOperators):
    #datetime.date object
    #key: if set, db query by uid: values can be uid or 0
    #weekly: true = week, false = day
    #fir: true/false
    
    #typeOfLocation gets its values as follows:
    # 0 = db query w/o area restriction
    # 1 = db query by postal code
    # 2 = db query by city name
    # more to be added
    
    #timeWindow: how many days of data is fetched (if fir=true, this doesn't matter)
    #resolution: averages are calculated for every [resolution] hours, values 1-24
    #sortOperators: true/false, whether separation of operators is desired.
    
    #some data alteration needed if key is postal code
    if typeOfLocation == 1:
        location = location + "%"
    
    #time is altered to include the given day
    time = time + timedelta(days = 1)
    
    if sortOperators:
        data = getAveragesSortOperators(time, key, location, typeOfLocation, weekly, fir, timeWindow, resolution, sortOperators)
    elif fir:
        data = getAveragesWeekFir(time, key, location, typeOfLocation, timeWindow, resolution, sortOperators)
    elif weekly:
        data = calculateAveragesWeekly(time, key, location, typeOfLocation, timeWindow, resolution, sortOperators,0,0)
    else:
        data = calculateAveragesDaily(time, key, location, typeOfLocation, timeWindow, resolution, sortOperators)
    return data

def getAveragesSortOperators(time, key, location, typeOfLocation, weekly, fir, timeWindow, resolution, sortOperators):   
    #This function is used if operator sorting is needed.
    allData = []
    for operator in ["Elisa","Sonera","DNA"]:
        if fir:
            data = getAveragesWeekFir(time, key, location, typeOfLocation, timeWindow, resolution, operator)
        elif weekly:
            data = calculateAveragesWeekly(time, key, location, typeOfLocation, timeWindow, resolution, operator,0,0)
        else:
            data = calculateAveragesDaily(time, key, location, typeOfLocation, timeWindow, resolution, operator)
            
        allData.append(data)
    return allData
    
def getAveragesWeekFir(time, key, location, typeOfLocation, timeWindow, resolution, sortOperators):
    #This function calculates weekly averages, and also takes into account the previous 3 weeks 
    #as a simple FIR filter.
    for i in range(1,5):
            
        data = getFromDataBase(time, key, location, typeOfLocation, -7,sortOperators)
        newData = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
        
        if i == 1:
            values = calculateAveragesWeekly(0,0,0,0,0,resolution,0,1,newData)
            for line in values:
                line[-1] += 1
            
        elif i == 2:
            temp = calculateAveragesWeekly(0,0,0,0,0,resolution,0,1,newData)
            for line in range(len(temp)):
                values[line][2] += temp[line][2] * 0.05
                values[line][3] += temp[line][3] * 0.05
                values[line][4] += temp[line][4] * 0.05
                values[line][5] += temp[line][5]
                values[line][-1] += 0.05
            
        elif i == 3:
            temp = calculateAveragesWeekly(0,0,0,0,0,resolution,0,1,newData)
            for line in range(len(temp)):
                values[line][2] += temp[line][2] * 0.025
                values[line][3] += temp[line][3] * 0.025
                values[line][4] += temp[line][4] * 0.025
                values[line][5] += temp[line][5]
                values[line][-1] += 0.025
            
        elif i == 4:
            temp = calculateAveragesWeekly(0,0,0,0,0,resolution,0,1,newData)
            for line in range(len(temp)):
                values[line][2] += temp[line][2] * 0.025
                values[line][3] += temp[line][3] * 0.025
                values[line][4] += temp[line][4] * 0.025
                values[line][5] += temp[line][5]
                values[line][-1] += 0.025
                
        time = time - timedelta(days = 7)
    
    for line in values:
        if line[-1]:
            line[2] = line[2] / line[-1]
            line[3] = line[3] / line[-1]    
            line[4] = line[4] / line[-1]
        line.pop(-1)

    return values

def calculateAveragesDaily(time,key,location, typeOfLocation,timeWindow,resolution,sortOperators):  
    
    data = getFromDataBase(time, key, location, typeOfLocation, timeWindow,sortOperators)
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

def calculateAveragesWeekly(time,key,location,typeOfLocation,timeWindow,resolution,sortOperators,filter,data):  
    
    if not filter:
        data = getFromDataBase(time, key, location, typeOfLocation, timeWindow,sortOperators)
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
    
    if not filter:
        averages = [i for i in averages if i[-1]]
    else:
        for line in averages:
            line.append(float(0))
    return averages

if __name__ == '__main__':
    #time = datetime.date object
    time = datetime.date(2016,6,1)
    #key = uid or 0
    key = 0
    #location: city or postal code
    location = "Espoo"
    #typeOfData as follows:
    # 0 = db query w/0 area restriction
    # 1 = db query by postal code
    # 2 = db query by city
    typeOfLocation = 2
    #from how many days datais acquired
    timeWindow = -70
    #averages are calculated for every [resolution] hours, values 1-24
    resolution = 1
    #use fir calculation or not, true/false
    fir = 1
    #sort by operators, true/false
    sortOperators = 0
    #weekly or daily averages, true=weekly/false=daily
    weekly = 1
    data = getAverages(time, key, location, typeOfLocation, weekly, fir, timeWindow, resolution, sortOperators)
    print(data)
    
    drawGraph(data)