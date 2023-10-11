import numpy as np

class Element:

    V = np.zeros(6)

    #v1, v2, v3, v4, v5, v6 = 0, 0, 0, 0, 0, 0

    def __init__(self, elemRow, n):
        self.elem_n = n # Elementnummer
        self.P1 = elemRow[0] # Globalt knutepunktnummer for ende 1
        self.P2 = elemRow[1] # Globalt knutepunktnummer for ende 2
        self.EModul = elemRow[2] # E-modul
        self.tType = elemRow[3] # Tverrsnittype, 1 = I-profil og 2 = rundprofil

        self.lenElem = np.sqrt((self.P1[0]-self.P2[0])**2 + (self.P1[1]-self.P2[1])**2) # Finner lengden til elementene med Pytagoras

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
    
