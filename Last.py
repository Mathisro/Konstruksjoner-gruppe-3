import numpy as np

class Last:

     def __init__(self, n, lastRow):
        self.lastn = n # Lastnummer 
        if lastRow[0] != 1: # Hvis fordelt last
            self.distLoad = True
            self.intencity = lastRow[6] # Intensiteten er gitt av en funksjon
            self.startPoint = np.array([lastRow[1], lastRow[2]]) # Startpunkt (x, y)
            self.endPoint = np.array([lastRow[3], lastRow[4]]) # Sluttpunkt (x, y)
            self.direction = lastRow[5] # Retning gitt som vinkel
            self.type = lastRow[0] # Type fordelt last: (Som med superposisjon kan gi alle muligheter)
            # 1 = punktlast, 2 = jevnt fordelt, 3 = trekant maks til høyre ytterst, 4 = trekant m/ maks venstre ytterst
            # 5 = trekant venstre maks innerst, 6 = trekant høyre maks innesrt , 7 = parabel, 8 = sinus
                
        
        else:
            self.distLoad = False
            self.intencity = lastRow[6] # Intensiteten gitt som en skalar
            self.attackPoint = np.array([lastRow[1], lastRow[2]]) # Angrepspunkt gitt som et punkt (x, y)
            self.direction = lastRow[5] # Retning gitt som en vinkel (x, y)

        # self.angle = -np.arctan2(self.direction[1], self.direction[0])
        self.angle = np.pi*self.direction/180