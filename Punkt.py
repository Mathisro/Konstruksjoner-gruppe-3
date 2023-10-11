class Punkt:

    def __init__(self, PunktRow, n):
        self.punktn = n # Punktnummer
        self.x = PunktRow[0] # x-koordinat
        self.y = PunktRow[1] # y-koordinat
        self.boundryVal = [2] # Grensebetingelse