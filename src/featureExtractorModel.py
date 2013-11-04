from collections import Counter
import util, datetime

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
    timeRecord = util.convertTimeStampToDate(_tempFeatureList[0])
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

    # featureDict['time'] = hour*60+minute
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

    dist = 0
    if locationDict[_tempFeatureList[1]]: 
        lat, lng = locationDict[_tempFeatureList[1]]  
        lotLocation = (float(lat), float(lng))
        #print "centroid", CENTROIDS[0]
        dist = min( [util.calculateDistance(lotLocation, (util.CENTROIDS[0][i], util.CENTROIDS[1][i]) ) for i in range(len(util.CENTROIDS[0])) ])        
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
    