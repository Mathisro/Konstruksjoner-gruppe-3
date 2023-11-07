import numpy as np

class Last:

     def __init__(self, n, lastRow):
        self.lastn = n                                              # Lastnummer 
        if lastRow[0] != 0:                                         # Hvis fordelt last
            self.distLoad = True
            self.intencity = lastRow[6]                             # Største intensitet
            self.startPoint = np.array([lastRow[1], lastRow[2]])    # Startpunkt [x, y]
            self.endPoint = np.array([lastRow[3], lastRow[4]])      # Sluttpunkt [x, y]
            self.direction = lastRow[5]                             # Retning i grader
            self.type = lastRow[0]                                  # Type fordelt last
        
        else:
            self.distLoad = False                                   # Ikke fordelt last, punktlast
            self.intencity = lastRow[6]                             # Intensiteten
            self.attackPoint = np.array([lastRow[1], lastRow[2]])   # Angrepspunkt [x, y]
            self.direction = lastRow[5]                             # Retning i grader

        self.angle = np.pi*self.direction/180                       # Ender vinkel til radianer