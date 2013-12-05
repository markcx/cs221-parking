import numpy
import matplotlib.pyplot as plt
import cPickle as pickle

leave_params = (.5, .05)

def visualize_P_leave(leave_params):
    c1, c2 = leave_params
    PriceVec = numpy.linspace(0,10,5)
    PriceVecLegend = ['$'+str(price) for price in PriceVec]
    AvailNumVec = numpy.linspace(0,20,100)
    colors = ['r','b','g','k','c']
    for i, price in enumerate(PriceVec):
        lambda_leave = numpy.maximum(numpy.zeros(len(AvailNumVec)), c1*AvailNumVec - c2*price)
        P_leave = numpy.exp(-1*lambda_leave)
        plt.plot(AvailNumVec, P_leave,colors[i])
    plt.xlabel('# of Available Spots', fontsize=24)
    plt.ylabel('Probability of leaving', fontsize=24)
    plt.legend(PriceVecLegend, fontsize=18)
    plt.show()

# visualize_P_leave(leave_params)

def testPredictionResults():
    with open('testPredictionResults.p', 'rb') as fp:
        totalErrResults = pickle.load(fp)
    fp.close()

    Lots = list()
    availNumErrVec = list()
    priceErrVec = list()

    for item in totalErrResults:
        Lots.append(item[0])
        availNumErrVec.append(item[1])
        priceErrVec.append(item[2])

    plt.plot(availNumErrVec)
    plt.show()

    plt.plot(priceErrVec)
    plt.show()

testPredictionResults()
