import math, operator, re, os, datetime, time
from collections import Counter


CENTROIDS = [[  37.80674047,   37.75915639,   37.77783732,   37.79128318,   37.78229867,
    37.79388065,   37.79965323,   37.78684646],
 [-122.41744638, -122.42047599, -122.42060377, -122.40172484, -122.39375636,
  -122.39602712, -122.43842723, -122.43269398]]

def calculateDistance(loc1, loc2, unit='mile'):
    """
    Calculating the distance between the location1 and location2 in miles
    show the

    """
    lat1, lng1 = loc1
    lat2, lng2 = loc2

    radius_km = 6371  # km
    radius_mile= 3960 # mile


    difflat = math.radians(lat2-lat1)
    difflng = math.radians(lng2-lng1)

    a = math.sin(difflat/2) * math.sin(difflat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(difflng/2) * math.sin(difflng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    if unit == 'mile':
        d = radius_mile * c
    elif unit == 'km':
        d = radius_km * c
    else:
        raise "none valid unit "

    return d



def extractRecordFeatures(x, locationDict, eventDict):
    """
    Extract the features from a string line 
    
    @param string 'x' : represents each timestamp there is a record 
    @return dictionary 
    
    Feature items:
        day - M, T, W, Th, F, S, Su    [7 entries]
        time - 6-10, 10-12, 12-14, 14-16, 16-18, 18-20, 20-22 [7 entries]
        loc - |loc - centroid|     [1 entry]
        price - 0 <= price , 1<= price, ..., 8 <= price  [9 entries] 
        events -   
         
         
    """ 
    featureDict =Counter()
    _tempFeatureList = [] 
    for item in x.split(','):
        #print "show items", item
        item = item.strip(' \"|\r|\n ')
        _tempFeatureList.append(item)
    

    # build feature vector phi
    timeRecord = convertTimeStampToDate(_tempFeatureList[0])
    # 
    day, hour, minute = timeRecord			
    
    initialHour = 6
    finalHour = 22
    # if earlier than 6am or later than 10pm, return empty feature  
    if hour < initialHour or hour >= finalHour:      
        return (featureDict, 0)
      
    dayDict = {0:'Mon', 1:'Tues', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
    
    assert day in dayDict

    # update the day feature
    featureDict[dayDict[day]] = 1  

    numTimeFeatures = (finalHour-initialHour)*2+1    # a feature every half hour

    for ind in range(numTimeFeatures):
        startHour = initialHour+ind/2
        finalHour = initialHour+(ind+1)/2
        if startHour == finalHour:
            startMin = 0
            endMin = 30
        else:
            startMin = 30
            endMin = 0

        startHourMin = startHour*60+startMin
        finalHourMin = finalHour*60+endMin

        actualHourMin = hour*60+minute

        if actualHourMin >= startHourMin and actualHourMin < finalHourMin:
            timeFeatureKey = str(startHour)+':'+str(startMin)+'-'+str(finalHour)+':'+str(endMin)
            featureDict[timeFeatureKey] = 1
            break

        

    # if timeRecord[0] == 0 :
    #     featureDict['Mon'] = 1        
    
    # elif timeRecord[0] == 1 :
    #     featureDict['Tue'] = 1 
        
    # elif timeRecord[0] == 2 :
    #     featureDict['Wed'] = 1        
    
    # elif timeRecord[0] == 3 :
    #     featureDict['Thu'] = 1 
    
    # elif timeRecord[0] == 4 :
    #     featureDict['Fri'] = 1 
    
    # elif timeRecord[0] == 5 :
    #     featureDict['Sat'] = 1 
    
    # elif timeRecord[0] == 6 :
    #     featureDict['Sun'] = 1 
    # else:
    #     raise "Error:[extractRecordFeatures] exception on weekday extraction"
       
    # if timeRecord[1] >=6 and timeRecord[1] < 8:    
    #     featureDict['6-8'] = 1       
    # elif timeRecord[1] >=8 and timeRecord[1] < 10:    
    #     featureDict['8-10'] = 1
    # elif timeRecord[1] >= 10 and timeRecord[1] < 12:    
    #     featureDict['10-12'] = 1
        
    # elif timeRecord[1] >= 12 and timeRecord[1] < 14:    
    #     featureDict['12-14'] = 1
        
    # elif timeRecord[1] >= 14 and timeRecord[1] < 16:    
    #     featureDict['14-16'] = 1
    # elif timeRecord[1] >= 16 and timeRecord[1] < 18:    
    #     featureDict['16-18'] = 1
    # elif timeRecord[1] >=18 and timeRecord[1] < 20:    
    #     featureDict['18-20'] = 1
    # elif timeRecord[1] >= 20 and timeRecord[1] < 22:         
    #     featureDict['20-22'] = 1
    # else:
    #     print "time record", timeRecord[1]
    #     raise "Error: [extractRecordFeatures] exception on hour extraction"
    
    dist = 0
    if locationDict[_tempFeatureList[1]]: 
        lat, lng = locationDict[_tempFeatureList[1]]  
        lotLocation = (float(lat), float(lng))
        #print "centroid", CENTROIDS[0]
        dist = min( [calculateDistance(lotLocation, (CENTROIDS[0][i], CENTROIDS[1][i]) ) for i in range(len(CENTROIDS[0])) ])        
    else:    
        dist = 0.5
    
    featureDict['Dist'] = dist 
        
    
    def checkEvent(timeTS):
        #print type(float(timeTS))
        currentTS = float(timeTS)
        for i in range(len(eventDict['ST'])):
            #print "Start TimeStamp",  eventDict['ST'][i], type(eventDict['ST'][i])
            #print currentTS > eventDict['ST'][i]
            #print currentTS < eventDict['ET'][i]
            if currentTS > eventDict['ST'][i] and currentTS < eventDict['ET'][i]:
                featureDict[eventDict['NAME'][i]] = 1
    
    
    
    def checkPrice(price, featureDict):
        currPrice = float(price) 
        #print "current price", currPrice        
        if currPrice < 0: 
            featureDict = Counter()
            return featureDict
        
        if currPrice >= 0 and currPrice < 1:
            featureDict['price_0-1'] = 1
        elif currPrice >= 1 and currPrice < 2:    
            featureDict['price_1-2'] = 1
        elif currPrice >= 2 and currPrice < 3:         
            featureDict['price_2-3'] = 1
        elif currPrice >= 3 and currPrice < 4:
            featureDict['price_3-4'] = 1
        elif currPrice >= 4 and currPrice < 5:    
            featureDict['price_4-5'] = 1
        elif currPrice >= 5 and currPrice < 6:
            featureDict['price_5-6'] = 1
        elif currPrice >= 6 and currPrice < 7:    
            featureDict['price_6-7'] = 1    
        else:
            featureDict['price_gte7'] = 1                         
    
    checkEvent(_tempFeatureList[0]) # here call the internal function to check the events feature    
    checkPrice(_tempFeatureList[-1], featureDict)
    

    # extract label y
    if int(_tempFeatureList[3]) < 0 or int(_tempFeatureList[2]) < 0 :
        avlNum = -99        
    else:
        avlNum = int(_tempFeatureList[3]) - int(_tempFeatureList[2])    
    
    
    return (featureDict, avlNum)
    

def convertTimeStampToDate(ts=None):
    ts = ts.strip(" \" ")
    if (ts is not None) and ( int(ts) > 100000):
        dateT = datetime.datetime.fromtimestamp(int(ts)) 
        y = dateT.year
        m = dateT.month
        d = dateT.day
    
        dayInWeek = datetime.date(y, m, d).weekday()   
        hourInDay = dateT.hour
	minInHour = dateT.minute    
        return (dayInWeek, hourInDay, minInHour)        
    
    return (-1, -1)    
    

def sparseVectorDotProduct(v1, v2):
    """
        Given two sparse vectors |v1| and |v2|, each represented as Counters, return
        their dot product.
        You might find it useful to use sum() and a list comprehension.
        """
    # BEGIN_YOUR_CODE (around 4 lines of code expected)
    #raise Exception("Not implemented yet")
    #dotResult = Counter()  #only above 2.7+
    
    summation = 0
    
    if len(v1)>len(v2):
        #temp=Counter()
        temp=v2
        v2=v1
        v1=temp
    #swap to make sure v1 has fewer entries
    
    for key in v1:
        if v2[key]:
            summation += v1[key]*v2[key]
     	    
    return summation 


    
def readFileUpdateWeight( filepath = 'NA', locDict='NA', eventDict='NA', weightsVector='NA', alpha=0.9):
    '''
    Reads each line in the filepath and update weightsVector (a Counter obj representing
    sparse vector) by stochastic gradient descent
        w[i] = w[i] + alpha*(y[i]-dotProd(w,phi))*phi[i]

    '''
    _weightsVector = weightsVector.copy()
    
    if not os.path.exists(filepath):    
        raise "File doesn't exist!!"
        return _weightsVector
    else:
        fp = open(filepath, 'r')
        for line in fp:
            phi, y = extractRecordFeatures(line, locDict, eventDict) 
            #print "take a look at the feature:",phi 
            if len(phi) <= 0 or y < 0 :    # if nothing changed for this line
                continue    
            
            dotProd = sparseVectorDotProduct(phi, _weightsVector)
            for key in phi:
                print "-------",y-dotProd
                _weightsVector[key]  =  _weightsVector[key] + alpha * (y - dotProd) * phi[key]
        fp.close()  
    
    return _weightsVector

       
class ReadLocation():
    def __init__(self, filepath='NA'):
        """
        reading the location file and returns a dictionary
        key = lot id
        val = corresponding (latitude, longitude)
        
        """
        
        if not os.path.exists(filepath):
            raise "file is not exist!!"
            return None
        else:
            self.filepath = filepath
            self.locationDict = dict()

        fp = open(self.filepath, 'r')
        
        for line in fp:
            _str = line.strip("\(|\)|\r|\n")
            _tempList = _str.split(', ')  
            
            offStreetID = _tempList[1].strip("\'") 
            onStreetID = _tempList[2].strip("\'")
            
            
            if int(offStreetID) > 0:        
                self.locationDict[str(offStreetID)] = ( _tempList[3].strip("\(|\'"), _tempList[4].strip("\'") ) 
            
            elif int(onStreetID) > 0:
                self.locationDict[str(onStreetID)] = ( _tempList[3].strip("\(|\'"), _tempList[4].strip("\'") ) 
            
            else:
                print "on street id", onStreetID
                
        fp.close
          
    def getLocationDict(self):
        if len(self.locationDict) > 0:
            return self.locationDict
        else:
            return [] 
        
        
class ReadEvents():
    def __init__(self, filepath='NA'):
        '''
        Reads the file containing all the events, and create three event dictionaries,
        with keys 
            ST - start time
            ET - end time
            NAME - name of event (Giants, Race, or Concert)
        and values a list of events

        e.g. For event i, 
            eventDict['NAME'][i] = name of event i
            eventDict['ST'][i] = start time of event i
            eventDict['ET'][i] = end time of event i
        '''


        self.eventDict = dict() 
        if not os.path.exists(filepath):
            raise "file is not exist!!"
            return None
        else:
            self.filepath = filepath
                  
            
            eventSTlist= []
            eventETlist= []
            eventNamelist=[]
            
            fp = open(self.filepath, 'r') 

            for line in fp:
               _tempLines = line.split('\r')                        
               for record in _tempLines:    
                   dateStr, startT, endT, event = record.split(',')  # date - m/d/y, start time, end time, event    
                   eventName = event.split()
                   #print "what event", eventName[-1]
                   #print dateStr, eventName[-1]     
                   m, d, y = dateStr.split('/')
                   y = '20'+y           
                   if startT.find("AM")>0:
                       st_str = startT.strip("AM")  
                       st_hh, st_mm = st_str.split(':')
                       st_hh = int(st_hh)                         
                   elif startT.find('PM')>0: 
                       st_str = startT.strip("PM")    
                       st_hh, st_mm = st_str.split(':')
                       if int(st_hh) != 12:
                           st_hh = int(st_hh)+12
                       else:
                           st_hh = int(st_hh)
                   #print "startT,",startT
                   #print "endT,", endT.strip("PM")
                   if endT.find('AM')>0:
                       et_str = endT.strip("AM")
                       et_hh, et_mm = et_str.split(':')
                       et_hh = int(et_hh) 
                       
                   elif endT.find('PM')>0:
                       et_str = endT.strip("PM")
                       et_hh, et_mm = et_str.split(':')                        
                       if int(et_hh) != 12:
                           et_hh = int(et_hh) + 12
                       else:
                           et_hh = int(et_hh)
                       
                   if type(st_hh) is int and type(et_hh) is int:
                       _dt1 = datetime.datetime(int(y), int(m), int(d), st_hh, int(st_mm))
                       _dt2 = datetime.datetime(int(y), int(m), int(d), et_hh, int(et_mm))
                   
                       ts1 = time.mktime(_dt1.timetuple())
                       ts2 = time.mktime(_dt2.timetuple())
                       #print ts1, ts2, eventName[-1]
                       eventSTlist.append(ts1)
                       eventETlist.append(ts2)
                       eventNamelist.append(eventName[-1])
                   
                   
            fp.close()
            
            #update dict            
            self.eventDict['ST'] = eventSTlist           
            self.eventDict['ET'] = eventETlist
            self.eventDict['NAME'] = eventNamelist
            
    def getEventDict(self):
        return self.eventDict         
            
            
        
readLocation = ReadLocation("../idLocation/helloLocation.txt")         
locDict = readLocation.getLocationDict()
#print locDict 

readEvents = ReadEvents("../eventsSchedule/event_schedule2.csv")
eventDict = readEvents.getEventDict()

weights = Counter()

def readFileList(filepath):
    files = []
    for filename in os.listdir(filepath):
        files.append(filename)

    return files


files = readFileList("../output/935/")

#print len(files)
for i in range(3,48):
    #print ">>", files[i]
    _fname = "../output/935/"+files[i]
    #print _fname 
    weights = readFileUpdateWeight(_fname, locDict, eventDict, weights, 0.1)


print weights     

def test(filepath, locDict, eventDict, weightsVector):
    fp = open(filepath, 'r')
    count = 0
    sumErr = 0
    for line in fp:
        #print line
        phi, y = extractRecordFeatures(line,locDict, eventDict)

        if len(phi)<=0 or y < 0:
            continue

        estimate = sparseVectorDotProduct(weightsVector, phi)
	print "==========show feature vector==========",phi 
        print "real", y, "est:", estimate, "diff error", y-estimate
        print "error rate", (y-estimate)/y
        count +=1
        sumErr += abs(y-estimate) / y
        
    fp.close()
    avgErr = sumErr/count
    print "--average error rate--", avgErr

    

test("../output/935/935_2013_09_17.csv", locDict, eventDict, weights)



#readfLearn = ReadingFileExtractFeatures("output/930/930_2013_08_05.csv", locDict, eventDict)        
#readfLearn.runRegression()        
        
        
        
