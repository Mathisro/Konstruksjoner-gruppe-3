import numpy as np
import Last

class Element:

    def harLast(self):                          # Sjekker om et element har ytre last
        return self.last != []
    
    def finnTverrsnitt(self, tverrOb, tsnitt):  # Finner tverrsnittobjekt gitt nummer for tverrsnittgeometrien
        for row in tverrOb:
            if row.type == tsnitt:
                return row
    

    def __init__(self, n, elemRow, PunktOb, tverrsnittOb):          # Initialiserer klassen
        self.elem_n = n                                             # Elementnummer
        self.P1 = PunktOb[int(elemRow[1])]                          # Globalt knutepunkt av typen Punkt for ende 1
        self.P2 = PunktOb[int(elemRow[2])]                          # Globalt knutepunkt av typen Punkt for ende 2
        self.tType = elemRow[3]                                     # Tverrsnittnummer for geometri
        self.tSnitt = self.finnTverrsnitt(tverrsnittOb, self.tType) # Tverrsnitt av klassen Tverrsnitt
        self.E = self.tSnitt.E                                      # E-modul
        self.f_y = elemRow[-1]                                      # Flytspenning

        self.L = np.linalg.norm(self.P1.punkt - self.P2.punkt)      # Lengden til elementene
        self.angle = np.arctan2((self.P2.punkt[1]-self.P1.punkt[1]),(self.P2.punkt[0]-self.P1.punkt[0])) # Vinkel i globalt system

        A = self.tSnitt.A   # Tverrsnittareal
        I = self.tSnitt.I   # Arealtreghetsmoment

        EI = I * self.E
        EA = A * self.E
        L = self.L

        self.k = np.array([np.array([EA/L , 0          , 0         , -EA/L, 0           , 0         ]),     # Lokal konnektivitetsmatrise K
                           np.array([0    , 12*EI/L**3 , -6*EI/L**2, 0    , -12*EI/L**3 , -6*EI/L**2]),
                           np.array([0    , -6*EI/L**2 , 4*EI/L    , 0    , 6*EI/L**2   , 2*EI/L    ]),
                           np.array([-EA/L, 0          , 0         , EA/L , 0           , 0         ]),
                           np.array([0    , -12*EI/L**3, 6*EI/L**2 , 0    , 12*EI/L**3  , 6*EI/L**2 ]),
                           np.array([0    , -6*EI/L**2 , 2*EI/L    , 0    , 6*EI/L**2   , 4*EI/L    ])])
        
    
        self.kTab = np.array([np.array([0, self.P1, 3 * (self.P1.punktn) + 0]), # Konnektivitetstabell
                              np.array([1, self.P1, 3 * (self.P1.punktn) + 1]),
                              np.array([2, self.P1, 3 * (self.P1.punktn) + 2]),
                              np.array([3, self.P2, 3 * (self.P2.punktn) + 0]),
                              np.array([4, self.P2, 3 * (self.P2.punktn) + 1]),
                              np.array([5, self.P2, 3 * (self.P2.punktn) + 2])])
        
        self.last = []                  # Liste over ytre laster
        self.fastInnMom = np.zeros(6)   # Lokale faste innspenningskrefter

        self.M, self.V, self.N = np.array([]), np.array([]), np.array([]) # Initialiserer lister for diagrammer

        self.rotMat = np.array([np.array([np.cos(self.angle) , np.sin(self.angle) , 0, 0                  , 0                  , 0]),   # Rotasjonsmatrise
                                np.array([-np.sin(self.angle), np.cos(self.angle) , 0, 0                  , 0                  , 0]),
                                np.array([0                  , 0                  , 1, 0                  , 0                  , 0]),
                                np.array([0                  , 0                  , 0, np.cos(self.angle) , np.sin(self.angle) , 0]),
                                np.array([0                  , 0                  , 0, -np.sin(self.angle), np.cos(self.angle) , 0]),
                                np.array([0                  , 0                  , 0, 0                  , 0                  , 1])])

    def indexFromKtab(self, index):             # Finne index fra konnektivitetstabell
        return self.kTab[:, 2][index]

    def transformFromGlobal(self, array):       # Transformerer vektor til lokale koordinater
        return np.matmul(self.rotMat, array)
    
    def transformToGlobal(self, array):         # Transformerer vektor til lokale koordinater
        return np.matmul(np.transpose(self.rotMat), array)
    
    def transformKToGlobal(self):               # Transformerer konnektivitetsmatrisen til globale koordinater
        return np.matmul(np.transpose(self.rotMat), np.matmul(self.k, self.rotMat))