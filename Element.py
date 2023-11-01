import numpy as np

class Element:

    V = np.zeros(6)

    def __init__(self, n, elemRow, PunktOb, tverrsnittOb):
        self.elem_n = n # Elementnummer
        self.P1 = PunktOb[int(elemRow[1])]  # Globalt knutepunkt av typen Punkt for ende 1
        self.P2 = PunktOb[int(elemRow[2])]  # Globalt knutepunkt av typen Punkt for ende 2           # E-modul
        self.tType = elemRow[3]             # Tverrsnittype, 1 = I-profil og 2 = rundprofil
        self.tSnitt = tverrsnittOb[int(self.tType)-1]
        self.E = self.tSnitt.E              # E-modul

        self.L = np.linalg.norm(self.P1.punkt - self.P2.punkt) # Finner lengden til elementene med Pytagoras
        self.angle = np.arctan2((self.P2.punkt[1]-self.P1.punkt[1]),(self.P2.punkt[0]-self.P1.punkt[0])) 

        A = self.tSnitt.A
        I = self.tSnitt.I

        EI = I * self.E
        EA = A * self.E
        L = self.L

        self.k = np.array([np.array([EA/L , 0          , 0         , -EA/L, 0           , 0         ]),
                           np.array([0    , 12*EI/L**3 , -6*EI/L**2, 0    , -12*EI/L**3 , -6*EI/L**2]),
                           np.array([0    , -6*EI/L**2 , 4*EI/L    , 0    , 6*EI/L**2   , 2*EI/L    ]),
                           np.array([-EA/L, 0          , 0         , EA/L , 0           , 0         ]),
                           np.array([0    , -12*EI/L**3, 6*EI/L**2 , 0    , 12*EI/L**3  , 6*EI/L**2 ]),
                           np.array([0    , -6*EI/L**2 , 2*EI/L    , 0    , 6*EI/L**2   , 4*EI/L    ])])
        
    
        self.kTab = np.array([np.array([0, self.P1, 3 * (self.P1.punktn) + 0]), # Med nullindeksering
                              np.array([1, self.P1, 3 * (self.P1.punktn) + 1]),
                              np.array([2, self.P1, 3 * (self.P1.punktn) + 2]),
                              np.array([3, self.P2, 3 * (self.P2.punktn) + 0]),
                              np.array([4, self.P2, 3 * (self.P2.punktn) + 1]),
                              np.array([5, self.P2, 3 * (self.P2.punktn) + 2])])

    def indexFromKtab(self, index):
        return self.kTab[:, 2][index]


    def rotMat(self, angle): # Definerer rotasjonsmatrisa for å transformere koordinatsystemene
        return np.array([np.array([np.cos(angle) , np.sin(angle) , 0, 0             , 0             , 0]),
                         np.array([-np.sin(angle), np.cos(angle) , 0, 0             , 0             , 0]),
                         np.array([0             , 0             , 1, 0             , 0             , 0]),
                         np.array([0             , 0             , 0, np.cos(angle) , np.sin(angle) , 0]),
                         np.array([0             , 0             , 0, -np.sin(angle), np.cos(angle) , 0]),
                         np.array([0             , 0             , 0, 0             , 0             , 1])])

    def transformFromGlobal(self, array): # Definerer transformasjon fra globale til lokale koordinater
        return np.matmul(self.rotMat(self.angle), array)
    
    def transformToGlobal(self, array): # Definerer transformasjon fra globale til lokale koordinater
        return np.matmul(np.transpose(self.rotMat(self.angle)), array)
    
    def transformKToGlobal(self):
        return np.matmul(np.transpose(self.rotMat(self.angle)), np.matmul(self.k, self.rotMat(self.angle)))
