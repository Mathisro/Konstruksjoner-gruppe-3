import numpy as np

class Element:

    V = np.zeros(6)



    #v1, v2, v3, v4, v5, v6 = 0, 0, 0, 0, 0, 0

    def __init__(self, n, elemRow, PunktOb, tverrsnittOb):
        self.elem_n = n # Elementnummer
        self.P1 = PunktOb[int(elemRow[0])]  # Globalt knutepunkt av typen Punkt for ende 1
        self.P2 = PunktOb[int(elemRow[1])]  # Globalt knutepunkt av typen Punkt for ende 2           # E-modul
        self.tType = elemRow[2]             # Tverrsnittype, 1 = I-profil og 2 = rundprofil
        self.tSnitt = tverrsnittOb[int(self.tType)-1]
        self.E = self.tSnitt.E              # E-modul

        self.L = np.linalg.norm(self.P1.punkt - self.P2.punkt) # Finner lengden til elementene med Pytagoras
        self.angle = np.arctan2((self.P2.punkt[1]-self.P1.punkt[1]),(self.P2.punkt[1]-self.P1.punkt[1])) # Skal alle indexene være 1?

        A = self.tSnitt.A
        I = self.tSnitt.I

        self.k = np.array([np.array([A*self.E/self.L  , 0                    , 0                    , -A*self.E/self.L, 0                      , 0                    ]),
                           np.array([0                , 12*self.E*I/self.L**3, -6*self.E*I/self.L**2, 0               , -12*self.E*I/self.L**3 , -6*self.E*I/self.L**2]),
                           np.array([0                , -6*self.E*I/self.L**2, 4*self.E*I/self.L    , 0               , 6*self.E*I/self.L**2   , 2*self.E*I/self.L    ]),
                           np.array([-A*self.E/self.L , 0                    , 0                    , A*self.E/self.L , 0                      , 0                    ]),
                           np.array([0                , 12*self.E*I/self.L**3, 6*self.E*I/self.L**2 , 0               , 12*self.E*I/self.L**3  , 6*self.E*I/self.L**2 ]),
                           np.array([0                , -6*self.E*I/self.L**2, 2*self.E*I/self.L    , 0               , 6*self.E*I/self.L**2   , 4*self.E*I/self.L    ])])

    
        self.kTab = np.array([np.array([0, self.P1, 3 * (self.P1.punktn) + 0]), # Med nullindeksering
                              np.array([1, self.P1, 3 * (self.P1.punktn) + 1]),
                              np.array([2, self.P1, 3 * (self.P1.punktn) + 2]),
                              np.array([3, self.P2, 3 * (self.P2.punktn) + 0]),
                              np.array([4, self.P2, 3 * (self.P2.punktn) + 1]),
                              np.array([5, self.P2, 3 * (self.P2.punktn) + 2])])


    def rotMat(self, angle): # Definerer rotasjonsmatrisa for å transformere koordinatsystemene
        return np.array([np.array([np.cos(angle) , np.sin(angle) , 0, 0             , 0             , 0]),
                         np.array([-np.sin(angle), np.cos(angle) , 0, 0             , 0             , 0]),
                         np.array([0             , 0             , 1, 0             , 0             , 0]),
                         np.array([0             , 0             , 0, np.cos(angle) , np.sin(angle) , 0]),
                         np.array([0             , 0             , 0, -np.sin(angle), np.cos(angle) , 0]),
                         np.array([0             , 0             , 0, 0             , 0             , 1])])

    def transformFromGlobal(self, angle, array): # Definerer transformasjon fra globale til lokale koordinater
        return np.matmul(self.rotMat(angle), array)
    
    def transformToGlobal(self, angle, array): # Definerer transformasjon fra globale til lokale koordinater
        return np.matmul(np.transpose(self.rotMat(angle)), array)
    
    def transformKToGlobal(self):
        return np.matmul(np.transpose(self.rotMat(self.angle)), np.matmul(self.k, self.rotMat(self.angle)))
