import math, os, datetime, time

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

def readFileList(filepath):
    '''
    Returns a list of all filenames in a folder
    '''
    files = []
    for filename in os.listdir(filepath):
        files.append(filename)

    return files


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
        
        