import math, operator, re, os, datetime, time
from collections import Counter
import util
import featureExtractorModel as model  
    

# linear regression algorithm
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
            phi, y = model.extractRecordFeatures(line, locDict, eventDict) 
            #print "take a look at the feature:",phi 
            if len(phi) <= 0 or y < 0 :    # if nothing changed for this line
                continue    
            
            dotProd = util.sparseVectorDotProduct(phi, _weightsVector)
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
        phi, y = model.extractRecordFeatures(line,locDict, eventDict)

        if len(phi)<=0 or y < 0:
            continue

        estimate = util.sparseVectorDotProduct(weightsVector, phi)
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
        
        
        
