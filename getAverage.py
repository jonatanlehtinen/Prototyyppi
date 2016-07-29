import mysql.connector as mariadb
from _datetime import date, datetime, timedelta
import datetime
from sockjs.tornado.stats import MovingAverage
from astropy.table.bst import MinValue


def getFromDataBase(time, key, location, typeOfLocation, lengthOfTime, operator):
      
    try:
        #Create connection to database
        mariadb_connection = mariadb.connect(user='root', password='pythontesti', database='postcodes')
        cursor = mariadb_connection.cursor()
        
        if typeOfLocation == 0:      
            #Query for data 
            #Select data from certain time window and possibly key
            if not key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s", (time,lengthOfTime, time,))
            elif key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s",(time,lengthOfTime,time,key,))
            elif not key and operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND networkoperator = %s",(time,lengthOfTime,time,operator,))
            else:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s AND networkoperator = %s",(time,lengthOfTime,time,key,operator))

        if typeOfLocation == 1:
            #Query for data 
            #Select data from certain time window and postal code
            if not key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND postalcode LIKE %s", (time,lengthOfTime, time,location,))
            elif key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s AND postalcode LIKE %s",(time,lengthOfTime,time,key,location,))
            elif not key and operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND networkoperator = %s AND postalcode LIKE %s",(time,lengthOfTime,time,operator,location))
            else:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s AND networkoperator = %s AND postalcode LIKE %s",(time,lengthOfTime,time,key,operator,location))

        if typeOfLocation == 2:
            #Select data from certain time window and city
            if not key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND county = %s", (time,lengthOfTime, time,location,))
            elif key and not operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s AND county = %s",(time,lengthOfTime,time,key,location,))
            elif not key and operator:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND networkoperator = %s AND county = %s",(time,lengthOfTime,time,operator,location))
            else:
                cursor.execute("SELECT startedAt, uid, latency, downlink, uplink, postalcode, networkoperator FROM espoohelsinkidata WHERE startedAt BETWEEN adddate(%s,%s) AND %s AND uid = %s AND networkoperator = %s AND county = %s",(time,lengthOfTime,time,key,operator,location))
            
        #More querys can be added here
        
        mariadb_connection.close()
        #return list including fetched data
        return list(cursor)

    except:
        print("Couldn't create database connection")
        return []

    
def getAverages(time, key, location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators):
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
        data = getAveragesSortOperators(time, key, location, typeOfLocation, longTime, weekly, fir, timeWindow, resolution, sortOperators)
    elif longTime:
        data = getAveragesLongTime(time, key, location, typeOfLocation, sortOperators)
    elif fir:
        data = getAveragesWeekFilter(weekly, time, key, location, typeOfLocation, timeWindow, resolution, sortOperators)
    elif weekly:
        data = calculateAveragesWeekly(time, key, location, typeOfLocation, timeWindow, resolution, sortOperators,0,0)
    else:
        data = calculateAveragesDaily(time, key, location, typeOfLocation, timeWindow, resolution, sortOperators,0,0)
    return data

def getAveragesSortOperators(time, key, location, typeOfLocation,longTime, weekly, fir, timeWindow, resolution, sortOperators):   
    #This function is used if operator sorting is needed.
    allData = []
    for operator in ["Elisa","Sonera","DNA"]:
        if longTime:
            data = getAveragesLongTime(time, key, location, typeOfLocation, operator)
        elif fir:
            data = getAveragesWeekFilter(weekly, time, key, location, typeOfLocation, timeWindow, resolution, operator)
        elif weekly:
            data = calculateAveragesWeekly(time, key, location, typeOfLocation, timeWindow, resolution, operator,0,0)
        else:
            data = calculateAveragesDaily(time, key, location, typeOfLocation, timeWindow, resolution, operator,0,0)
        
        allData.append(data)
    return allData

def getAveragesLongTime(time, key, location, typeOfLocation, sortOperators):
    
    data = getFromDataBase(time, key, location, typeOfLocation, -180, sortOperators)
    data = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
    data.sort(key=lambda x: (x[0]))
    averages = []
    
    maxVal = max([i[3] for i in data])
    minVal = 0.025*maxVal
    maxVal = 0.975*maxVal
    data = [i for i in data if i[3] < maxVal and i[3] > minVal] 
    
    for item in data:
        if datetime.date(item[0].year, item[0].month, item[0].day) not in [i[0] for i in averages]:
            averages.append([])
            averages[-1].append(datetime.date(item[0].year, item[0].month, item[0].day))
            averages[-1].append(item[3])
            averages[-1].append(item[4])
            averages[-1].append(item[2])
            averages[-1].append(1)
        else:
            i = [i[0] for i in averages].index(datetime.date(item[0].year, item[0].month, item[0].day))
            averages[i][1] += item[3]
            averages[i][2] += item[4]
            averages[i][3] += item[2]
            averages[i][4] += 1
            
    for item in averages:
        item[1] = item[1] / item[4]
        item[2] = item[2] / item[4]
        item[3] = item[3] / item[4]
    
    movingAverage = [[[],[],[],[],[]] for i in range(len(averages)-10)]
    
    for i in range(5,len(movingAverage)+5):
        movingAverage[i-5][0] = averages[i][0]
        movingAverage[i-5][4] = averages[i][4]
        movingAverage[i-5][1] = (averages[i-3][1] + averages[i-2][1] + averages[i-1][1] + averages[i][1] + averages[i+1][1] + averages[i+2][1] + averages[i+3][1]) / 7
        movingAverage[i-5][2] = (averages[i-3][2] + averages[i-2][2] + averages[i-1][2] + averages[i][2] + averages[i+1][2] + averages[i+2][2] + averages[i+3][2]) / 7
        movingAverage[i-5][3] = (averages[i-3][3] + averages[i-2][3] + averages[i-1][3] + averages[i][3] + averages[i+1][3] + averages[i+2][3] + averages[i+3][3]) / 7
    
    averages = movingAverage
    return averages
   
def getAveragesWeekFilter(weekly, time, key, location, typeOfLocation, timeWindow, resolution, sortOperators):
    #This function calculates weekly averages, and also takes into account the previous 3 weeks 
    #as a simple FIR filter.
    
    if weekly: 
        val = 2
    else:
        val = 1
    
    for i in range(1,11):
        if weekly:
            data = getFromDataBase(time, key, location, typeOfLocation, -7, sortOperators)
        else:
            data = getFromDataBase(time, key, location, typeOfLocation, -1, sortOperators)
            
        newData = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
 
        if i == 1:
            if weekly:
                values = calculateAveragesWeekly(0,0,0,0,0,resolution,0,1,newData)
            else:
                values = calculateAveragesDaily(0,0,0,0,0,resolution,0,1,data)
            for line in values:
                line[-1] += 1
            
        else:
            if weekly:
                temp = calculateAveragesWeekly(0,0,0,0,0,resolution,0,1,newData)
            else:
                temp = calculateAveragesDaily(0,0,0,0,0,resolution,0,1,newData)
            if i > 1 and i < 4:
                weight = 0.1
            elif i < 7:
                weight = 0.05
            else:
                weight = 0.025
            
            for line in range(len(temp)):
                values[line][val] += temp[line][val] * weight
                values[line][val+1] += temp[line][val+1] * weight
                values[line][val+2] += temp[line][val+2] * weight
                values[line][val+3] += temp[line][val+3]
                values[line][-1] += weight
        
        if weekly:    
            time = time - timedelta(days = 7)
        else:
            time = time-timedelta(days = 1)
    
    for line in values:
        if line[-1]:
            line[val] = line[val] / line[-1]
            line[val+1] = line[val+1] / line[-1]    
            line[val+2] = line[val+2] / line[-1]
        line.pop(-1)
        
    return values

def calculateAveragesDaily(time,key,location,typeOfLocation,timeWindow,resolution,sortOperators,filter,data):  
    
    if not filter:
        data = getFromDataBase(time, key, location, typeOfLocation, timeWindow,sortOperators)
        data = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
        data.sort(key=lambda x: (x[0]))
    
    averages = []
    
    maxVal = max([i[3] for i in data])
    minVal = 0.025*maxVal
    maxVal = 0.975*maxVal
    data = [i for i in data if i[3] < maxVal and i[3] > minVal] 
           
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
    
    
    movingAverage = [[[],[],[],[],[]] for i in range(len(averages))]
    
    for i in range(len(movingAverage)):
        movingAverage[i][0] = averages[i][0]
        movingAverage[i][4] = averages[i][4]
        
        if i == len(movingAverage)-1:
            temp1 = 1
            temp = 0
        elif i == len(movingAverage) -2:
            temp1 = i+1
            temp = 0
        else:
            temp1 = i+2
            temp = i+1   
            
        movingAverage[i][1] = (averages[i-2][1] + averages[i-1][1] + averages[i][1] + averages[temp][1] + averages[temp1][1]) / 5
        movingAverage[i][2] = (averages[i-2][2] + averages[i-1][2] + averages[i][2] + averages[temp][2] + averages[temp1][2]) / 5
        movingAverage[i][3] = (averages[i-2][3] + averages[i-1][3] + averages[i][3] + averages[temp][3] + averages[temp1][3]) / 5
    
    averages = movingAverage
    
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
    
    if not filter:
        averages = [i for i in averages if i[-1]]
    else:
        for line in averages:
            line.append(float(0))
    return averages
       	
    return averages

def calculateAveragesWeekly(time,key,location,typeOfLocation,timeWindow,resolution,sortOperators,filter,data):  
    
    if not filter:
        data = getFromDataBase(time, key, location, typeOfLocation, timeWindow,sortOperators)
        data = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
        data.sort(key=lambda x: (x[0]))
    averages = []
    
    maxVal = max([i[3] for i in data])
    minVal = 0.025*maxVal
    maxVal = 0.975*maxVal
    data = [i for i in data if i[3] < maxVal and i[3] > minVal]
    
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
    
    movingAverage = [[[],[],[],[],[],[]] for i in range(len(averages))]
    
    for i in range(len(movingAverage)):
        movingAverage[i][0] = averages[i][0]
        movingAverage[i][1] = averages[i][1]
        movingAverage[i][5] = averages[i][5]
        
        if i == len(movingAverage)-1:
            temp1 = 1
            temp = 0
        elif i == len(movingAverage) -2:
            temp1 = i+1
            temp = 0
        else:
            temp1 = i+2
            temp = i+1   
                
        movingAverage[i][2] = (averages[i-2][2] + averages[i-1][2] + averages[i][2] + averages[temp][2] + averages[temp1][2]) / 5
        movingAverage[i][3] = (averages[i-2][3] + averages[i-1][3] + averages[i][3] + averages[temp][3] + averages[temp1][3]) / 5
        movingAverage[i][4] = (averages[i-2][4] + averages[i-1][4] + averages[i][4] + averages[temp][4] + averages[temp1][4]) / 5
        
    averages = movingAverage

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
