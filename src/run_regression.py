import math, operator, re, os
from collections import Counter
import util
import featureExtractorModel as model  
import cPickle as pickle
import json

lots = ['935', '202031', '326052']
# lots = os.listdir('../data')      # get a list of all lots in train directory

readLocation = util.ReadLocation("../idLocation/helloLocation.txt")         
locDict = readLocation.getLocationDict()

readEvents = util.ReadEvents("../eventsSchedule/event_schedule2.csv")
eventDict = readEvents.getEventDict()

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
            if len(phi) <= 0 or y < 0 :    # if nothing changed for this line
                continue    
            
            dotProd = util.sparseVectorDotProduct(phi, _weightsVector)
            for key in phi:
                # print "-------",y-dotProd
                _weightsVector[key]  =  _weightsVector[key] + alpha * (y - dotProd) * phi[key]
        fp.close()  
    
    return _weightsVector

def printingWeights(weights):
    for key in weights:
        print key, weights[key]

def linearRegression(lot):
    '''
    Run linear regression on |lot| and save the weights to file

    |lot| is a string denoting the lotID, e.g. lot='935'
    '''
    weights = Counter()

    files = util.readFileList("../data/"+lot)

    # for i in range(3,48):
    for _fname in files:
        
        if _fname[-9:-7] == '07' or _fname[-9:-7] == '08':  # only train on Jul and Aug data
            # print _fname
            # _fname = "../train/"+lot+"/"+files[i]
            weights = readFileUpdateWeight(_fname, locDict, eventDict, weights, 0.1) 

    # write weights to file
    with open('../weights/'+lot+'weights.p', 'wb') as fp:
        pickle.dump(weights, fp)
    fp.close()

    with open('../weights/'+lot+'weights.json', 'wb') as fp:
        json.dump(weights, fp)
    fp.close()
    printingWeights(weights)

# run regression on all the lots
for lot in lots:
    linearRegression(lot)
        
