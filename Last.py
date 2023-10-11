import numpy as np

class Last:

     def __init__(self, lastRow, n):
        self.lastn = n # Lastnummer 
        if lastRow[0]: # Hvis jevnt fordelt last
            self.intencity = lastRow[1] # Intensiteten er gitt av en funksjon
            self.startpoint = lastRow[2] # Startpunkt (x, y)
            self.endpoint = lastRow[3] # Sluttpunkt (x, y)
#           self.direction = lastRow[4]    <-- Unødvendig, virker alltid rett på? I grader?

        else:
            self.intencity = lastRow[1] # Intensiteten gitt som en skalar
            self.attackPoint = lastRow[2] # Angrepspunkt gitt som et punkt (x, y)
            self.direction = lastRow[3] # Retning gitt som en retningsvektor (x, y)