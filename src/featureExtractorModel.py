from collections import Counter
import util, datetime

initialHour = 6
finalHour = 22

#### Still need to add:
# - implement previous day feature
#     - if predicting next day
#     - keep track of list of prediction for each day for one week
#         - list comprehension of local averages
# - discretize other feature - done
#     <.2
#     <.4
# - change learning rate - done
#     - alpha = 1/t^.5

def getTimeFeatureEveryNHour(N):
    timeFeature = list()
    numTimeFeatures = (finalHour-initialHour)/N    # a feature every half hour
    assert numTimeFeatures >= 1
    endHour = initialHour
    for ind in range(numTimeFeatures):
        startHour = endHour
        endHour = startHour+N
        startMin = 0
        endMin = 0
        timeFeature.append(((startHour, startMin), (endHour, endMin)))
        # timeFeatureKey = str(startHour)+':'+str(startMin)+'-'+str(endHour)+':'+str(endMin)
        # print timeFeatureKey
    return timeFeature

def getTimeFeatureEveryNMin(N):
    '''
    return the designed time feature, where time is spaced every N minutes. 
    Assert that 60 is divisible by N
    '''
    n = 60/N
    timeFeature = list()
    numTimeFeatures = (finalHour-initialHour)*n    # a feature every half hour
    for ind in range(numTimeFeatures):
        startHour = initialHour+ind/n
        endHour = initialHour+(ind+1)/n
        whichMin = ind % n
        startMin = N*whichMin
        endMin = N*(whichMin+1)
        if endMin == 60:
            endMin = 0
        timeFeature.append(((startHour, startMin), (endHour, endMin)))
    return timeFeature

timeFeature10min = getTimeFeatureEveryNMin(10)
timeFeature20min = getTimeFeatureEveryNMin(20)
timeFeature30min = getTimeFeatureEveryNMin(30)
# print timeFeature30min
timeFeature1hr = getTimeFeatureEveryNHour(1)
timeFeature2hr = getTimeFeatureEveryNHour(2)

# for i in range(len(timeFeature30min)):
#     startTuple, endTuple = timeFeature30min[i]
# for startTuple, endTuple in timeFeature30min:
#     print startTuple, endTuple
#     startHour, startMin = startTuple
#     print startHour, startMin
#     endHour, endMin = endTuple

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
    
    # if earlier than 6am or later than 10pm, return empty feature  
    if hour < initialHour or hour >= finalHour:      
        return (featureDict, 0, 0)
      
    dayDict = {0:'Mon', 1:'Tues', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
    
    assert day in dayDict

    # update the day feature
    featureDict[dayDict[day]] = 1  

    # update time feature
    def updateTimeFeature(timeFeature):
        # print '-----'
        # print timeFeature
        # print len(timeFeature)
        # for i in range(len(timeFeature)):
        #     print i
        #     startTuple, endTuple = timeFeature[i]
        
        for startTuple, endTuple in timeFeature:
            # print startTuple, endTuple
            startHour, startMin = startTuple
            endHour, endMin = endTuple


            startHourMin = startHour*60+startMin
            finalHourMin = endHour*60+endMin

            actualHourMin = hour*60+minute
            # print actualHourMin
            # print startHourMin, finalHourMin

            if actualHourMin >= startHourMin and actualHourMin < finalHourMin:
                timeFeatureKey = str(startHour)+':'+str(startMin)+'-'+str(endHour)+':'+str(endMin)
                featureDict[timeFeatureKey] = 1
                # print timeFeatureKey
                break

    # updateTimeFeature(timeFeature10min)
    updateTimeFeature(timeFeature20min)
    # updateTimeFeature(timeFeature30min)
    # updateTimeFeature(timeFeature1hr)
    updateTimeFeature(timeFeature2hr)

    dist = 0
    if locationDict[_tempFeatureList[1]]: 
        lat, lng = locationDict[_tempFeatureList[1]]  
        lotLocation = (float(lat), float(lng))
        #print "centroid", CENTROIDS[0]
        dist = min( [util.calculateDistance(lotLocation, (util.CENTROIDS[0][i], util.CENTROIDS[1][i]) ) for i in range(len(util.CENTROIDS[0])) ])        
    else:    
        dist = 0.5
    
    def updateDistFeature(dist, interval=.2, max_miles=5):
        '''
        Returns indicator functions for distance, in intervals of |interval| miles, up to |max_miles| miles

        feature is 1 if dist <= _d
        '''
        _d = 0
        while _d < max_miles:
            _d += interval
            if dist <= _d:
                featureDict['Dist<='+str(_d)] = 1

    featureDict['Dist'] = dist 
    # updateDistFeature(dist, .2, 5)
        
    
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
    # checkPrice(currPrice, featureDict)
    currPrice = float(_tempFeatureList[-1])    # current price

    checkEvent(_tempFeatureList[0]) # here call the internal function to check the events feature    

    # extract label y
    if int(_tempFeatureList[3]) < 0 or int(_tempFeatureList[2]) < 0 :
        avlNum = -99        
    else:
        avlNum = int(_tempFeatureList[3]) - int(_tempFeatureList[2])    
    

    return (featureDict, avlNum, currPrice)
    