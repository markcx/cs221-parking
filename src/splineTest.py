# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 21:14:14 2013

@author: markxchen
"""

import numpy as np
import scipy as sp
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

'''
x1 = sorted([1., 0.88, 0.67, 0.50, 0.35, 0.27, 0.18, 0.11, 0.08, 0.04, 0.04, 0.02])
y1 = [0., 13.99, 27.99, 41.98, 55.98, 69.97, 83.97, 97.97, 111.96, 125.96, 139.95, 153.95]
 



new_length = 25
new_x = np.linspace(min(x1),  max(x1), new_length)
new_y = sp.interpolate.interp1d(x1, y1, kind='cubic')(new_x)

plt.plot(x1,y1,'o', new_x, new_y , '--' )

'''

data=[]
index=[]
f = open('mean.csv')
i = 0
for line in f:
    i +=1    
    a = line.split()   
    data.append(float(a[1])) 
    ind = float(i)/float(12)
    index.append(ind)
    
    
f.close()

#print data

y1 = np.array(data)

x1 = np.array(index)

xRescale = x1
print y1 , "x", xRescale
xnew = np.linspace(min(xRescale),max(xRescale), 10)

func = sp.interpolate.interp1d(xRescale,y1)          

# suppose y2 (numpy array) is value at Sept 3, then
spline_y = func(x1)
error = sum((spline_y-y2)*(spline_y-y2)/y2)
print error

plt.plot(xRescale,y1, 'b', xnew, func(xnew),'r--',  )
plt.xlabel('Time 0:00 - 24:00',fontsize=12)     
plt.ylabel('Occupancy Ratio ')          
plt.legend(['Historical Average','Spline Fit'])

# = sp.interpolate.interp1d(x1, y1, kind='cubic') 

'''
    newTestData=[]
    index2 =[]
    f2 = open('foo2.csv')
    i = 0
    for line in f2:
    i +=1
    a = line.split()
    newTestData.append(float(a[1]))
    ind = float(i)/float(12)
    index2.append(ind)
    f2.close()
    #print data
    
    
    print "------------",func(xnew)
    y2 = np.array(newTestData)
    spline_y = func(x1)
    print spline_y
    error = sum((spline_y-y2)*(spline_y-y2)/y2)
    print error
    # 0.125880036804
'''    
    
   