import numpy as np

class Element:

    V = np.zeros(6)

    #v1, v2, v3, v4, v5, v6 = 0, 0, 0, 0, 0, 0

    def __init__(self, n, elemRow, PunktOb):
        self.elem_n = n # Elementnummer
        self.P1 = PunktOb[int(elemRow[0])] # Globalt knutepunkt av typen Punkt for ende 1
        self.P2 = PunktOb[int(elemRow[1])] # Globalt knutepunkt av typen Punkt for ende 2
        self.EModul = elemRow[2] # E-modul
        self.tType = elemRow[3] # Tverrsnittype, 1 = I-profil og 2 = rundprofil

        self.lenElem = np.linalg.norm(self.P1.punkt - self.P2.punkt) # Finner lengden til elementene med Pytagoras
        self.angle = np.arctan2((self.P2.punkt[1]-self.P1.punkt[1]),(self.P2.punkt[1]-self.P1.punkt[1])) # Skal alle indexene være 1?

    def rotMat(angle): # Definerer rotasjonsmatrisa for å transformere koordinatsystemene
        return np.array([np.array([np.cos(angle) , np.sin(angle) , 0, 0             , 0             , 0]),
                         np.array([-np.sin(angle), np.cos(angle) , 0, 0             , 0             , 0]),
                         np.array([0             , 0             , 1, 0             , 0             , 0]),
                         np.array([0             , 0             , 0, np.cos(angle) , np.sin(angle) , 0]),
                         np.array([0             , 0             , 0, -np.sin(angle), np.cos(angle) , 0]),
                         np.array([0             , 0             , 0, 0             , 0             , 1])])

    def transformFromGlobal(self, angle, array): # Definerer transformasjon fra globale til lokale koordinater
        return np.matmul(self.rotMat(angle), array) # self.v? self.rotmat?
    
    def transformToGlobal(self, angle, array): # Definerer transformasjon fra globale til lokale koordinater
        return np.matmul(np.transpose(self.rotMat(angle)), array)
    
