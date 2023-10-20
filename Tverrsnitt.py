import numpy as np

class Tverrsnitt:

    def __init__(self, tverrsnitt):
        self.E = tverrsnitt[10]
        
        if tverrsnitt[1] == 0: # Høyden er null --> Rørprofil
            self.A = np.pi * (tverrsnitt[4]**2 - tverrsnitt[5]**2) # Ytre diameter minus indre diameter
            self.I = 0.25 * np.pi (tverrsnitt[4]**4 - tverrsnitt[5]**4)
        elif tverrsnitt[7] != 0: # Tykkelse flens oppgitt --> I-profil
            h = tverrsnitt[1]
            b = tverrsnitt[3]
            tf = tverrsnitt[7]
            ts = tverrsnitt[8]

            self.A = 2*b * tf + (h-2*tf) * ts
            self.I = (b*h**3 - (b-ts)*(h-tf)**3)/12

        elif tverrsnitt[4] == 0 and tverrsnitt[6] == 0: # Ingen indre bredde og høyde oppgitt --> Massivt profil
            h = tverrsnitt[1]
            b = tverrsnitt[3]

            self.A = h*b
            self.I = (b*h**3)/12

        else: 
            H = tverrsnitt[1]
            h = tverrsnitt[2]
            B = tverrsnitt[3]
            b = tverrsnitt[4]

            self.A = H*B - h*B
            self.I = (B*H**3)/12 - (b*h**3)/12
        