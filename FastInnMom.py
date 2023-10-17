import numpy as np

class FastInnMom:

    def dist(p1, p2, p3): # Finner avstanden fra linjen mellom to punkter (et element) til et punkt (angrepspunkt)
        return np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
    
    def fibPair(pair):                                                 # Finner fastinnspenningsmoment for endepunktene til et element
        if not pair[0].distload:    
            P = pair[0].intencity                                      # Intensitet på lasten
            phi = pair[0].angle - pair[1].angle                        # Lastens vinkel på alement
            a = np.linalg.norm(pair[0].attackPoint - pair[1].P1.punkt) # Avtand fra last til P1
            b = np.linalg.norm(pair[0].attackPoint - pair[1].P2.punkt) # Avstand fra last til P2
            L = pair[1].lenElem                                        # Elementlengde
            M1 = -(P * np.sin(phi) * a * b**2)/L                       # Fast innspenningsmoment i P1 (Globalt knutepunkt nr. index1)
            M2 = (P * np.sin(phi) * a**2 * b)/L
            q1 = M1 + M2 + P  * a
            q2 = P - q1
            return M1, M2, q1, q2
        else:
            p = pair[0].intencity
            phi = pair[0].angle - pair[1].angle
            L = pair[1].lenElem 
            a = np.linalg.norm(pair[0].startPoint - pair[1].P1.punkt) # Avtand fra last til P1
            b = L - np.linalg.norm(pair[0].endPoint - pair[1].P1.punkt)
            s = np.linalg.norm(pair[0].startPoint - pair[0].endPoint)
            M1 = -((s+a)**2 * (6*b**2+4*b*(s+a)+(s+a)**2) + s**2*(6*(s+b)**2+4*a*(s+b)+a**2))*p*np.sin(phi)/(12*L^2)
          

    def __init__(self, lastOb, elemOb, npunkt, nelem):
        self.fib = np.zeros(npunkt) # Systemlastvektor med fast innspenningsmoment og last.
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
            M1, M2, q1, q2 = self.fibPair(pair)
            index1R = 3*pair[1].P1.punktn + 1           # Index moment i ende 1 i Systemlastvektor-vektor
            index2R = 3*pair[1].P2.punktn + 1           # Index for moment i ende to i Systemlastvektor
            self.fib[index1R] = M1                      # Fast innspenningsmoment i P1 (Globalt knutepunkt nr. index1)
            self.fib[index1R + 1] = q1                  # Fast innspenningslast i P1
            self.fib[index2R] = M2                      # Fast innspenningsmoment i P2 (Globalt knutepunkt nr. index2)
            self.fib[index2R + 1] = q2                  # Fast innspenningslast i P2

    