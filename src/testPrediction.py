from collections import Counter
import util
import featureExtractorModel as model 
import cPickle as pickle

lot = '935'
with open('../weights/'+lot+'weights.p', 'rb') as fp:
    weights = pickle.load(fp)
print weights

readEvents = util.ReadEvents("../eventsSchedule/event_schedule2.csv")
eventDict = readEvents.getEventDict()

readLocation = util.ReadLocation("../idLocation/helloLocation.txt")         
locDict = readLocation.getLocationDict()

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

