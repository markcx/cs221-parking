import os, util, re, math
import ParkingMDP
import blackJackSubmission as submission
import cPickle as pickle
import featureExtractorModel as model 

'''
say user wants to go to:
	AT&T Park
	Pier 39
	Market St
'''

DestLocation = {
	'AT&T Park': (37.778635,-122.39051),
	'Pier 39': (37.805105,-122.416376),
	'Civic Center': (37.781162,-122.4132)
}


def filterLotsByMaxDist(final_dest, max_dist):
	lots = os.listdir('../data')      # get a list of all lots in output directory
	locDict = util.locDict
	lots_within_max_dist = list()
	for lot in lots:
		lotLocation = tuple(float(v) for v in locDict[lot])
		dist = util.calculateDistance(final_dest, lotLocation)
		
		if dist <= max_dist:
			# print lot, lotLocation, dist
			lots_within_max_dist.append(lot)

	# print len(lots_within_max_dist)
	return lots_within_max_dist

# filterLotsByMaxDist(DestLocation['AT&T Park'],.5)

def parseArrivalTime(arrival_time):
	day = arrival_time[3:5]		# in string
	hour = int(arrival_time[7:9])	# in int
	minute = int(arrival_time[10:])	# in int

	return (day, hour, minute)

def predictLot(filename, time, AvailNum_weightsVector, Price_weightsVector, lotid, lotLocation, final_dest):
	'''
	Predicts the availNum and price at |time| by averaging the prediction result from (time-timeBuffer) to (time)

	Returns a tuple of the prediction result
	'''

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
			phi, availNum, price = model.extractRecordFeatures(line,util.locDict, util.eventDict)
			if len(phi)<=0 or availNum < 0 or price < 0:
			    continue
			availNumEstimate += round(util.sparseVectorDotProduct(AvailNum_weightsVector, phi))
			priceEstimate += util.sparseVectorDotProduct(Price_weightsVector, phi)

	# averaging
	availNumEstimate /= count
	priceEstimate /= count

	dist = util.calculateDistance(final_dest, lotLocation)	# distance between lot and final location

	return (lotid, lotLocation, round(availNumEstimate), priceEstimate, dist)


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

	c1, c2 = (.5, .05)

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
		# print filename
		lotResult = predictLot(filename, (hour, minute), AvailNum_weightsVector, Price_weightsVector, lot, lotLocation, final_dest)

		lotResultVec.append(lotResult)

		lambda_leave = max(0, c1*lotResult[2] - c2*lotResult[3])
		# print lotResult[0], lotResult[2], lotResult[3], math.exp(-1*lambda_leave)

	return lotResultVec

def runMDP(lotResultVec, user_input, leave_params):
	arrival_time, final_dest, max_dist, max_price, pref = user_input
	mdp = ParkingMDP.SmartParkingMDP(pref, leave_params, lotResultVec)
	vi = submission.ValueIteration()
	vi.solve(mdp)
	print 'best actions'

	visitedVec = list()
	# for state in vi.pi:
		# print state
		# Visited, currLotIndex, IsEnd = state
		# print sum(Visited), type(sum(Visited))
		# visitedVec.append(sum(Visited))

		# if sum(Visited) == 1 and currLotIndex >= 0  and IsEnd == 0:
			# print Visited, currLotIndex, IsEnd

		# if currLotIndex >= 0  and IsEnd == 0:
		# 	print lotResultVec[currLotIndex][0], lotResultVec[currLotIndex][2], sum(Visited), vi.pi[state]

		# print state, vi.pi[state]
	# print vi.pi.values()
	# print sorted(visitedVec)

# user_input = ('09-03, 13:40', DestLocation['AT&T Park'], .5, 10, .3)
# lotResultVec = predictionForUser(user_input)
leave_params = (.5, .05)


# runMDP(lotResultVec, user_input, leave_params)







