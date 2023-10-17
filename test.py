#import structureVisualization
import numpy as np
import Punkt
import Last
import Element
import FastInnMom



npunkt = 2
punkt = np.array([np.array([0, 0, 0]),np.array([1, 0, 0])])
nelem = 1
elem = np.array([np.array([0, 1, 210e6, 1])])
nlast = 1
last = np.array([np.array([0, 10e3, (0.5, 0), (0, -1)])])

punktOb = []
for i in range(npunkt):
        punktOb.append(Punkt.Punkt(i, punkt[i]))
        
elementOb = []
for i in range(nelem):
        elementOb.append(Element.Element(i, elem[i], punktOb))

lastOb = []
for i in range(nlast):
        lastOb.append(Last.Last(i, last[i]))


fim = FastInnMom.FastInnMom(lastOb, elementOb, npunkt, nelem)

fimVector = fim.fib

print(fimVector)