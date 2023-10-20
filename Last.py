import numpy as np

class Last:

     def __init__(self, n, lastRow):
        self.lastn = n # Lastnummer 
        if lastRow[0]: # Hvis fordelt last
            self.distLoad = True
            self.intencity = lastRow[1] # Intensiteten er gitt av en funksjon
            self.startPoint = lastRow[2] # Startpunkt (x, y)
            self.endPoint = lastRow[3] # Sluttpunkt (x, y)
            self.direction = lastRow[4] # Retning gitt som retningsvektor
            self.type = lastRow[5] # Type fordelt last: (Som med superposisjon kan gi alle muligheter)
            # 1 = jevnt fordelt, 2 = trekant maks til høyre ytterst, 3 = trekant m/ maks venstre ytterst
            # 4 = trekant venstre maks innerst, 5 = trekant høyre maks innesrt , 8 = parabel, 7 = sinus
                
        
        else:
            self.distLoad = False
            self.intencity = lastRow[1] # Intensiteten gitt som en skalar
            self.attackPoint = lastRow[2] # Angrepspunkt gitt som et punkt (x, y)
            self.direction = lastRow[3] # Retning gitt som en retningsvektor (x, y)

        self.angle = -np.arctan2(self.direction[1], self.direction[0])