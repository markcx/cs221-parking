from collections import Counter
import util
import featureExtractorModel as model 
import cPickle as pickle
import matplotlib.pyplot as plt

lots = ['935', '202031', '326052']
# lots = os.listdir('../test')      # get a list of all lots in output directory

readEvents = util.ReadEvents("../eventsSchedule/event_schedule2.csv")
eventDict = readEvents.getEventDict()

readLocation = util.ReadLocation("../idLocation/helloLocation.txt")         
locDict = readLocation.getLocationDict()

def test(filename, locDict, eventDict, weightsVector):
    fp = open("../test"+filename, 'r')
    count = 0
    sumErr = 0

    Yvec = list()
    estimateVec = list()

    for line in fp:
        #print line
        phi, y = model.extractRecordFeatures(line,locDict, eventDict)

        if len(phi)<=0 or y < 0:
            continue

        estimate = util.sparseVectorDotProduct(weightsVector, phi)
        estimate = round(estimate)
        print "==========show feature vector==========",phi 
        print "real", y, "est:", estimate, "diff error", y-estimate

        if abs(y-estimate) < 1e-3:
            print "error rate", 0
            sumErr += 0
            count += 1
        elif y > 0:
            print "error rate", (y-estimate)/y
            count +=1
            sumErr += abs(y-estimate) / y

        Yvec.append(y)
        estimateVec.append(estimate)
        
    fp.close()
    avgErr = sumErr/count
    print "--average error rate--", avgErr

    plt.plot(Yvec,'b-')
    plt.plot(estimateVec,'r-')
    plt.legend(['real','prediction'])
    plt.ylabel('number of available spot')
    plt.title(filename)
    plt.show()

for lot in lots:
    # load the weights
    with open('../weights/'+lot+'weights.p', 'rb') as fp:
        weights = pickle.load(fp)
    fp.close()
    # print weights
    filename = "/"+lot+"/"+lot+"_2013_09_03.csv"

    test(filename, locDict, eventDict, weights)

