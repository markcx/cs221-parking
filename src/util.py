import math, datetime

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