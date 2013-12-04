import math, operator, re, os
from collections import Counter
import util
import featureExtractorModel as model  
import cPickle as pickle
import json

# lots = ['935', '202031', '326052']
lots = os.listdir('../data')      # get a list of all lots in train directory

readLocation = util.ReadLocation("../idLocation/helloLocation.txt")         
locDict = readLocation.getLocationDict()

readEvents = util.ReadEvents("../eventsSchedule/event_schedule2.csv")
eventDict = readEvents.getEventDict()

# linear regression algorithm
def readFileUpdateWeight(AvailNum_weightsVector, Price_weightsVector,  filepath = 'NA', locDict='NA', eventDict='NA', alpha=.5, eta_0=1.):
    '''
    Reads each line in the filepath and update weightsVector (a Counter obj representing
    sparse vector) by stochastic gradient descent, for predicting both AvailNum and Price
        w[i] = w[i] + eta*(y[i]-dotProd(w,phi))*phi[i]

    update learning rate by eta = eta_0/t^alpha
    '''
    # _AvailNum_weightsVector = AvailNum_weightsVector.copy()
    # _Price_weightsVector = Price_weightsVector.copy()
    if not os.path.exists(filepath):    
        raise "File doesn't exist!!"
        return _weightsVector
    else:
        fp = open(filepath, 'r')
        for t, line in enumerate(fp):
            eta = eta_0/(t+1)**alpha
            
            phi, availNum, currPrice = model.extractRecordFeatures(line, locDict, eventDict) 
            if len(phi) <= 0 or availNum < 0 or currPrice < 0:    # if nothing changed for this line
                continue    
            
            AvailNum_dotProd = util.sparseVectorDotProduct(phi, AvailNum_weightsVector)
            Price_dotProd = util.sparseVectorDotProduct(phi, Price_weightsVector)
            for key in phi:
                # print "-------",y-dotProd
                AvailNum_weightsVector[key]  += eta * (availNum - AvailNum_dotProd) * phi[key]
                Price_weightsVector[key]  += eta * (currPrice - Price_dotProd) * phi[key]
        fp.close()  
    
    return (AvailNum_weightsVector, Price_weightsVector)

def printingWeights(weights):
    for key in weights:
        print key, weights[key]

def linearRegression(lot):
    '''
    Run linear regression on |lot| and save the weights to file

    |lot| is a string denoting the lotID, e.g. lot='935'
    '''
     
    AvailNum_weightsVector = Counter()
    Price_weightsVector = Counter()

    files = util.readFileList("../data/"+lot)

    # for i in range(3,48):
    for _fname in files:
        
        if _fname[-9:-7] == '07' or _fname[-9:-7] == '08':  # only train on Jul and Aug data
            # print _fname
            # _fname = "../train/"+lot+"/"+files[i]
            AvailNum_weightsVector, Price_weightsVector = readFileUpdateWeight(AvailNum_weightsVector, Price_weightsVector, _fname, locDict, eventDict) 

    # write weights to file
    with open('../weights/'+lot+'AvailNumWeights.p', 'wb') as fp:
        pickle.dump(AvailNum_weightsVector, fp)
    fp.close()

    with open('../weights/'+lot+'AvailNumWeights.json', 'wb') as fp:
        json.dump(AvailNum_weightsVector, fp)
    fp.close()
    with open('../weights/'+lot+'Price_weights.p', 'wb') as fp:
        pickle.dump(Price_weightsVector, fp)
    fp.close()

    with open('../weights/'+lot+'Price_weights.json', 'wb') as fp:
        json.dump(Price_weightsVector, fp)
    fp.close()
    # printingWeights(weights)

# run regression on all the lots
for lot in lots:
    print lot
    linearRegression(lot)
        
