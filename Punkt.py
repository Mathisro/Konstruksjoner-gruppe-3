import numpy as np

class Punkt:

    def __init__(self, PunktRow, n):
        self.punktn = n # Punktnummer
        self.punkt = (PunktRow[0], PunktRow[1]) # Koordinater som tupple
#        self.x = PunktRow[0] # x-koordinat
#        self.y = PunktRow[1] # y-koordinat
        self.boundryVal = [2] # Grensebetingelse