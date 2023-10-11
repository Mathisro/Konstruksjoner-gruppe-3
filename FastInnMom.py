import numpy as np

class FastInnMom:

    def dist(p1, p2, p3): # Finner avstanden fra linjen mellom to punkter (et element) til et punkt (angrepspunkt)
        return np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)

    def __init__(self, lastOb, elemOb, npunkt, nelem):
        self.fib = np.zeros(npunkt) # Vektor med alle faste innspenningsmoment
        self.pairs = np.array([]*lastOb) # Matrise med alle ytre laster med tilhørende element

        for i in range(len(lastOb)): # Ønsker å sjekke om en last virker på et elemnt, for så å legge inn par i 'pairs'.
            if not lastOb[0].distLoad: # Hvis ikke fordelt last
                for j in range(nelem):
                    d = self.dist(elemOb[j].P1.punkt, elemOb[j].P2.punkt, lastOb[i].attakcPoint) # Avstand fra angrepspunkt til element
                    if d < 0.01: # Hvis angrepspunktet er på elementet
                        self.pairs[i] = (lastOb[i], elemOb[j])
            else:
                for j in range(nelem): 
                    d1 = self.dist(elemOb[j].P1.punkt, elemOb[j].P2.punkt, lastOb[i].startPoint) # Avstand fra startpunkt til element
                    d2 = self.dist(elemOb[j].P1.punkt, elemOb[j].P2.punkt, lastOb[i].endPoint) # Avstand fra sluttpunkt til element
                    if d1 + d2 < 0.02: # Hvis begge punkt ligger på elementet
                        self.pairs[i] = (lastOb[i], elemOb[j])

        for pair in self.pairs:
            if not pair[0].distload:
                index1 = pair[1].P1.punktn                                 # Elementnummer ende 1, P1
                index2 = pair[1].P2.punktn                                 # Elementnummer ende 2, P2
                P = pair[0].intencity                                      # Intensitet på lasten
                phi = pair[0].angle - pair[1].angle                        # Lastens vinkel på alement
                a = np.linalg.norm(pair[0].attackPoint - pair[1].P1.punkt) # Avtand fra last til P1
                b = np.linalg.norm(pair[0].attackPoint - pair[1].P2.punkt) # Avstand fra last til P2
                L = pair[1].lenElem                                        # Elementlengde
                self.fib[index1] = -(P * np.sin(phi) * a * b**2)/L         # Fast innspenningsmoment i P1 (Globalt knutepunkt nr. index1)
                self.fib[index2] = (P * np.sin(phi) * a**2 * b)/L          # Fast innspenningsmoment i P2 (Globalt knutepunkt nr. index2)

    