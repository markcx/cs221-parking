import os, util, re

def filterLotsByMaxDist(final_dest, max_dist):
	lots = os.listdir('../data')      # get a list of all lots in output directory
	# readLocation = util.ReadLocation("../idLocation/helloLocation.txt")         
	locDict = util.locDict
	lots_within_max_dist = list()
	for lot in lots:
		lotLocation = tuple(float(v) for v in locDict[lot])
		# t = tuple(int(v) for v in re.findall("[0-9]+", lotLocation))		
		dist = util.calculateDistance(final_dest, lotLocation)
		print lot, lotLocation, dist, type(lot)
		if dist <= max_dist:
			lots_within_max_dist.append(lot)

	return lots_within_max_dist

filterLotsByMaxDist((40,-120),2)

def parseArrivalTime(arrival_time):
	day = arrival_time[3:5]		# in string
	hour = int(arrival_time[7:9])	# in int
	minute = int(arrival_time[10:])	# in int

	return (day, hour, minute)

def predictLot(filename, time, AvailNum_weightsVector, Price_weightsVector, lotid, location, final_dest):
	fp = open("../data"+filename, 'r')
	HourMin = time[0]*60+time[1]
	timeBuffer = 10		# the time (in minutes), ahead of arrival_time, that we will consider when we do prediction
	count = 0

	availNumEstimate = 0.0
	priceEstimate = 0.0

	for line in fp:
		parsedLine = util.exactSingleLineFromFine(line)
		_, currHour, currMin = util.convertTimeStampToDate(parsedLine[0])
		currHourMin = currHour*60+currMin

		if HourMin - currHourMin <= timeBuffer:
			count += 1
	        phi, availNum, price = model.extractRecordFeatures(line,locDict, eventDict)
	        if len(phi)<=0 or availNum < 0 or price < 0:
	            continue
			availNumEstimate += round(util.sparseVectorDotProduct(AvailNum_weightsVector, phi))
			priceEstimate += round(util.sparseVectorDotProduct(Price_weightsVector, phi))

	# averaging
	availNumEstimate /= count
	priceEstimate /= count

	dist = util.calculateDistance(final_dest, lotLocation)	# distance between lot and final location

	return (lotid, location, availNumEstimate, priceEstimate, dist)


def predictionForUser(user_input):
	'''
	The user will input 
		(estimated time of arrival, final destination (as loc coord), 
		max_dist of walking (miles), max_price willing to pay ($), 
		preference for shortest dist or cheapest lot)
	
	Example:
		arrival_time = "09-03, 13:40"	# expressed in date, military time
		final_dest = (40,-120)
		max_dist = 2
		max_price = 3
		pref = .8	(prefer shortest dist 80% of the time)

	Run prediction to output list of lots
	'''
	locDict = util.locDict
	arrival_time, final_dest, max_dist, max_price, pref = user_input
	LotsToTry = filterLotsByMaxDist(final_dest, max_dist)	# filter to only a subset of lots to try

	day, hour, minute = parseArrivalTime(arrival_time)

	lotResultVec = list()
	for lot in LotsToTry:
		lotLocation = tuple(float(v) for v in locDict[lot])
	    # load the weights
	    with open('../weights/'+lot+'AvailNumWeights.p', 'rb') as fp:
	        AvailNum_weightsVector = pickle.load(fp)
	    fp.close()

	    with open('../weights/'+lot+'Price_weights.p', 'rb') as fp:
	        Price_weightsVector = pickle.load(fp)
	    fp.close()
	    
	    filename = "/"+lot+"/"+lot+"_2013_09_"+day+".csv"
	    print filename
	    lotResult = predictLot(filename, (hour, minute), AvailNum_weightsVector, Price_weightsVector, lot, lotLocation, final_dest)
	    
	    lotResultVec.append(lotResult)

	return lotResultVec





