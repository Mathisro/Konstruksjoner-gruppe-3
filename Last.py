import numpy as np

class Last:

     def __init__(self, lastRow, n):
        self.lastn = n # Lastnummer 
        if lastRow[0]: # Hvis fordelt last
            self.distLoad = lastRow[1] # Type fordelt last, 0 for jevnt fordelt, 1 for linjelast og 2 for parabel
            self.intencity = lastRow[2] # Intensiteten er gitt av en funksjon
            self.startpoint = lastRow[3] # Startpunkt (x, y)
            self.endpoint = lastRow[4] # Sluttpunkt (x, y)
            self.direction = lastRow[5]    
        
        else:
            self.distLoad = False
            self.intencity = lastRow[1] # Intensiteten gitt som en skalar
            self.attackPoint = lastRow[2] # Angrepspunkt gitt som et punkt (x, y)
            self.direction = lastRow[3] # Retning gitt som en retningsvektor (x, y)