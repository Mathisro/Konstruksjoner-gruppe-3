import numpy as np

class Kapasitet:

    def MisesSpenning(self, M, N, V, A, I, h):
        sigma_x = (np.array(M) / I) * h/2 + np.array(N)/A
        tau = np.array(V)/A # Tilnærming

        return np.sqrt(sigma_x**2 + 3*tau**2)
    
    def __init__(self, elemOb):
        self.kapasitet = []
        for elem in elemOb:
            mises = self.MisesSpenning(elem.M, elem.N, elem.V, elem.tSnitt.A, elem.tSnitt.I, elem.tSnitt.H)
            
            maxMises = np.max(mises)
            self.kapasitet.append(round(100* maxMises/(elem.f_y*1e6), 2))

