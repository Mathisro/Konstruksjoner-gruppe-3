import numpy as np

class Tverrsnitt:

    def __init__(self, tverrsnitt):
        self.E = tverrsnitt[10]
        self.type = tverrsnitt[0]
        
        if tverrsnitt[1] == 0: # Høyden er null --> Rørprofil
            D = tverrsnitt[5]
            d = tverrsnitt[6]
            #print(f'R = {R} og r = {r}')

            self.A = np.pi * ((D/2)**2 - (d/2)**2) # Ytre diameter minus indre diameter
            self.I = np.pi * (D**4 - d**4)/64
            self.H = D/2
        elif tverrsnitt[7] != 0: # Tykkelse flens oppgitt --> I-profil
            h = float(tverrsnitt[1])
            b = float(tverrsnitt[3])
            tf = float(tverrsnitt[7])
            ts = float(tverrsnitt[8])

            self.A = 2*b * tf + (h-2*tf) * ts
            self.I = (b*h**3 - (b-ts)*(h-tf*2)**3)/12
            self.H = h/2

        elif tverrsnitt[4] == 0 and tverrsnitt[6] == 0: # Ingen indre bredde og høyde oppgitt --> Massivt profil
            b = tverrsnitt[1]
            h = tverrsnitt[3]

            self.A = h*b
            self.I = (b*h**3)/12
            self.H = h/2

        else: 
            B = tverrsnitt[1]
            b = tverrsnitt[2]
            H = tverrsnitt[3]
            h = tverrsnitt[4]

            #print(f'B = {B}, b = {b}, H = {H}, h = {h}')

            self.A = H*B - h*b
            self.I = (B*H**3)/12 - (b*h**3)/12
            self.H = H/2

            #print(self.I)
        