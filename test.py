#import structureVisualization
import numpy as np
import Punkt
import Last
import Element



npunkt = 2
punkt = np.array([np.array([0, 0, 0]),np.array([1, 0, 0])])
nelem = 1
elem = np.array([np.array([0, 1, 210e6, 1])])
nlast = 1
last = np.array([0, 10e3, (0.5, 0), (0, -1)])

punktOb = np.zeros(npunkt)
for i in range(npunkt):
        punktOb[i] = Punkt.Punkt(i, punkt[i])
        
elementOb = np.zeros(nelem)
for i in range(nelem):
        elementOb[i] = Element.Element(i, elem[i])

lastOb = np.zeros(nlast)
for i in range(nlast):
        lastOb[i] = Last.Last(i, last[i])
