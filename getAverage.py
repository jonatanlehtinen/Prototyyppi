import MySQLdb as mariadb
from _datetime import date, datetime, timedelta
import datetime
import numpy


def getFromDataBase(time, key, location, typeOfLocation, lengthOfTime, operator):
    try:
        #Create connection to database
        mariadb_connection = mariadb.connect(user='netti', passwd='Passwd', db='nettitutka')
        cursor = mariadb_connection.cursor()
        print(key, time)
        print(location, typeOfLocation, lengthOfTime, operator)        
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

    
def getAverages(time, key, location, typeOfLocation, longTime, weekly, filter, timeWindow, resolution, sortOperators):
    #datetime.date object
    #key: if set, db query by uid: values can be uid or 0
    #weekly: true = week, false = day
    #filter: true/false
    
    #typeOfLocation gets its values as follows:
    # 0 = db query w/o area restriction
    # 1 = db query by postal code
    # 2 = db query by city name
    # more to be added
    
    #timeWindow: how many days of data is fetched (if filter=true, this doesn't matter)
    #resolution: averages are calculated for every [resolution] hours, values 1-24
    #sortOperators: true/false, whether separation of operators is desired.
    
    #some data alteration needed if key is postal code
    if typeOfLocation == 1:
        location = location + "%"
    
    #time is altered to include the given day
    time = time + timedelta(days = 1)
    
    #Different functions are called according to the parameters
    if sortOperators:
        data = getAveragesSortOperators(time, key, location, typeOfLocation, longTime, weekly, filter, timeWindow, resolution, sortOperators)
    elif longTime:
        data = getAveragesLongTime(time, key, location, typeOfLocation, sortOperators)
    elif filter:
        data = getAveragesWeekFilter(weekly, time, key, location, typeOfLocation, timeWindow, resolution, sortOperators)
    elif weekly:
        data = calculateAveragesWeekly(time, key, location, typeOfLocation, timeWindow, resolution, sortOperators,0,0)
    else:
        data = calculateAveragesDaily(time, key, location, typeOfLocation, timeWindow, resolution, sortOperators,0,0)
    return data

def getAveragesSortOperators(time, key, location, typeOfLocation,longTime, weekly, filter, timeWindow, resolution, sortOperators):   
    #This function is used if operator sorting is needed.
    #Averages are calculated for each operator separately.
    allData = []
    if sortOperators in ["Elisa","Sonera","DNA"]:
        if longTime:
            data = getAveragesLongTime(time, key, location, typeOfLocation, sortOperators)
        elif filter:
            data = getAveragesFilter(weekly, time, key, location, typeOfLocation, timeWindow, resolution, sortOperators)
        elif weekly:
            data = calculateAveragesWeekly(time, key, location, typeOfLocation, timeWindow, resolution, sortOperators,0,0)
        else:
            data = calculateAveragesDaily(time, key, location, typeOfLocation, timeWindow, resolution, sortOperators,0,0)
        allData = data
    else:
        for operator in ["Elisa","Sonera","DNA"]:
            if longTime:
                data = getAveragesLongTime(time, key, location, typeOfLocation, operator)
            elif filter:
                data = getAveragesFilter(weekly, time, key, location, typeOfLocation, timeWindow, resolution, operator)
            elif weekly:
                data = calculateAveragesWeekly(time, key, location, typeOfLocation, timeWindow, resolution, operator,0,0)
            else:
                data = calculateAveragesDaily(time, key, location, typeOfLocation, timeWindow, resolution, operator,0,0)
            allData.append(data)
    return allData

def movingaverage(data, window_size):
    #This function uses convolution to calculate moving average.
    window = numpy.ones(int(window_size))/float(window_size)
    return numpy.convolve(data, window, 'same')

def getAveragesLongTime(time, key, location, typeOfLocation, sortOperators):
    #This function is used to calculate long time averages, set to 180 days.
    #Data is fetched from database
    data = getFromDataBase(time, key, location, typeOfLocation, -180, sortOperators)
    data = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
    data.sort(key=lambda x: (x[0]))
    if not data:
        return False
    averages = []
    '''
    #The max and min download values from data are deleted.
    #2.5% of highest and lowest measures.
    maxVal = max([i[3] for i in data])
    minVal = 0.025*maxVal
    maxVal = 0.975*maxVal
    data = [i for i in data if i[3] < maxVal and i[3] > minVal] 
    '''
    #Averages for each day are calculated from data, and added to a new list.
    #The new list contains datetime, download ave, upload ave, latency ave and number of measurements.
    for item in data:
        #If datetime is not in averages yet, it will be appended.
        if datetime.date(item[0].year, item[0].month, item[0].day) not in [i[0] for i in averages]:
            averages.append([])
            averages[-1].append(datetime.date(item[0].year, item[0].month, item[0].day))
            averages[-1].append(item[3])
            averages[-1].append(item[4])
            averages[-1].append(item[2])
            averages[-1].append(1)
        #Otherwise, measured values are added.
        else:
            i = [i[0] for i in averages].index(datetime.date(item[0].year, item[0].month, item[0].day))
            averages[i][1] += item[3]
            averages[i][2] += item[4]
            averages[i][3] += item[2]
            averages[i][4] += 1
    
    #And then averages are calculated.       
    for item in averages:
        item[1] = item[1] / item[4]
        item[2] = item[2] / item[4]
        item[3] = item[3] / item[4]
    
    #After this, moving average is calculated to smoothen the data.
    #The time window is set to 11 days, +-5 days from the day of calculation.
    windowSize = 15
    
    #Movingaverage is called to download, upload and latency separately.
    movingAve = movingaverage([i[1] for i in averages], windowSize)
    for i in range(len(averages)):
        averages[i][1] = movingAve[i]
        
    movingAve = movingaverage([i[2] for i in averages], windowSize)
    for i in range(len(averages)):
        averages[i][2] = movingAve[i]
        
    movingAve = movingaverage([i[3] for i in averages], windowSize)
    for i in range(len(averages)):
        averages[i][3] = movingAve[i]
    
    #First and last 5 entries from averages are deleted. This is because
    #convolution lowers their values.   
    del averages[:7]
    del averages[-7:]
    
    return averages
   
def getAveragesFilter(weekly, time, key, location, typeOfLocation, timeWindow, resolution, sortOperators):
    #This function calculates weekly averages, and also takes into account the previous 9 weeks 
    #as a simple FIR filter.
    
    #Function acts a little different when the averages are calculated weekly.
    if weekly: 
        val = 2
    else:
        val = 1
    values = 0
    #This for loop loops the 10 weeks, that are used to calculate averages.
    for i in range(1,11):
        #Data is fetched from database. 7 days for weekly aves, 1 day for daily aves.
        if weekly:
            data = getFromDataBase(time, key, location, typeOfLocation, -7, sortOperators)
        else:
            data = getFromDataBase(time, key, location, typeOfLocation, -1, sortOperators)
            
        newData = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
        
        #The functions to calculate the averages are called during the first iteration of for loop.
        if i == 1 or not values:
            if newData:
                if weekly:
                    values = calculateAveragesWeekly(0,0,0,0,0,resolution,0,1,newData)
                else:
                    values = calculateAveragesDaily(0,0,0,0,0,resolution,0,1,data)
                for line in values:
                    line[-1] += 1
        #After the first iteration, this else clause is used.  
        else:
            if newData:
                if weekly:
                    temp = calculateAveragesWeekly(0,0,0,0,0,resolution,0,1,newData)
                else:
                    temp = calculateAveragesDaily(0,0,0,0,0,resolution,0,1,newData)
                #More older the data, less it weighs in the average.
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
                    if temp[line][val]:
                        values[line][-1] += weight
                    
                   
        #Time is moved back 7 or 1 days for the next iteration of for loop.
        if weekly:    
            time = time - timedelta(days = 7)
        else:
            time = time-timedelta(days = 1)
    
    #Averages are calulated and the total weight is removed.
    print(values)
    for line in values:
        if line[-1]:
            line[val] = line[val] / line[-1]
            line[val+1] = line[val+1] / line[-1]    
            line[val+2] = line[val+2] / line[-1]
        line.pop(-1)
        
    return values

def calculateAveragesDaily(time,key,location,typeOfLocation,timeWindow,resolution,sortOperators,filter,data):  
    #This function calculates the averages hourly for a length of a day.
    
    #Returns data in format
    #[hour, download, upload, latency, amount of measurements]
    
    #If this function is called by the filter, then it doesn't need to access the db.
    if not filter:
        data = getFromDataBase(time, key, location, typeOfLocation, timeWindow,sortOperators)
        data = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
        data.sort(key=lambda x: (x[0]))
    if not data:
        return False
    averages = []
    
    #The max and min download values from data are deleted.
    #2.5% of highest and lowest measures.
    maxVal = max([i[3] for i in data])
    minVal = 0.025*maxVal
    maxVal = 0.975*maxVal
    data = [i for i in data if i[3] < maxVal and i[3] > minVal] 
    
    #The list to store the average data is created.     
    for hour in range(0,24):
        averages.append([hour,0,0,0,0])
    
    #The data is handled and added to the list of averages.   
    for line in data:
        indexInAverages = line[0].hour
        
        averages[indexInAverages][1] += line[3]
        averages[indexInAverages][2] += line[4]
        averages[indexInAverages][3] += line[2]
        averages[indexInAverages][4] += 1
    
    #Averages are counted here.          
    for valueSet in averages:
        if valueSet[4]:
            valueSet[1] = valueSet[1] / valueSet[4]
            valueSet[2] = valueSet[2] / valueSet[4]
            valueSet[3] = valueSet[3] / valueSet[4]
    
    #Moving average is used to smoothen the data
    #window size of 5 is used, that is +-2 days
    windowSize = 5
    
    values = [i[1] for i in averages]
    movingAve = movingaverage(values[-2:]+values+values[:2], windowSize)
    for i in range(len(averages)):
        averages[i][1] = movingAve[i+2]
    
    values = [i[2] for i in averages]
    movingAve = movingaverage(values[-2:]+values+values[:2], windowSize)
    for i in range(len(averages)):
        averages[i][2] = movingAve[i]
    
    values = [i[3] for i in averages]    
    movingAve = movingaverage(values[-2:]+values+values[:2], windowSize)
    for i in range(len(averages)):
        averages[i][3] = movingAve[i]
        
        
    #resolution can be used to calculate averages for every 'res' hour.
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
    
    #if used by filter, one zero added for each data entry.
    #required by filter.
    if filter:
        for line in averages:
            line.append(float(0))
    return averages
       	

def calculateAveragesWeekly(time,key,location,typeOfLocation,timeWindow,resolution,sortOperators,filter,data):  
    #Calculates averages for every hour of the week.
    #The principle is the same as in calculateAveragesDaily
    
    #Returns data in form 
    #[day, hour, download, upload, latency, amount of meaurements]
    if not filter:
        data = getFromDataBase(time, key, location, typeOfLocation, timeWindow,sortOperators)
        data = [(item[0], item[1], item[2], item[3], item[4], item[5][:5], item[6]) for item in data]
        data.sort(key=lambda x: (x[0]))
    if not data:
        return False
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
    
    windowSize = 7
    
    values = [i[2] for i in averages]
    movingAve = movingaverage(values[-3:]+values+values[:3], windowSize)
    for i in range(len(averages)):
        averages[i][2] = movingAve[i+2]
    
    values = [i[3] for i in averages]
    movingAve = movingaverage(values[-3:]+values+values[:3], windowSize)
    for i in range(len(averages)):
        averages[i][3] = movingAve[i]
    
    values = [i[4] for i in averages]    
    movingAve = movingaverage(values[-3:]+values+values[:3], windowSize)
    for i in range(len(averages)):
        averages[i][4] = movingAve[i]
        
    
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
    
    if filter:
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
    #use filter calculation or not, true/false
    filter = 1
    #sort by operators, true/false
    sortOperators = 0
    #weekly or daily averages, true=weekly/false=daily
    weekly = 1
    data = getAverages(time, key, location, typeOfLocation, weekly, filter, timeWindow, resolution, sortOperators)
    print(data)
    
    drawGraph(data)
