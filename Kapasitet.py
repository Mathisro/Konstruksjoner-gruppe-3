import numpy as np

class Kapasitet:

    def MisesSpenning(self, M, N, V, A, I, h):                              # Regner ut Misesspenning
        sigma_x = (np.array(M) / I) * h/2 + np.array(N)/A                   # Normalspenning som sum av bøyespenning og aksialspenning
        tau = np.array(V)/A                                                 # Tilnærming til skjærspenning

        return np.sqrt(sigma_x**2 + 3*tau**2)                               # Misespenning i to dimensjoner
    
    def __init__(self, elemOb):                                             # Initialiserer objektet
        self.kapasitet = []
        for elem in elemOb:
            mises = self.MisesSpenning(elem.M, elem.N, elem.V, elem.tSnitt.A, elem.tSnitt.I, elem.tSnitt.H)
            
            maxMises = np.max(mises)                                        # Finner største misespenning på bjelken
            self.kapasitet.append(round(100* maxMises/(elem.f_y*1e6), 2))   # Regner ut utnyttelse som prosent av flyt

