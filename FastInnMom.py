import numpy as np

class FastInnMom:

    def dist(self, p1, p2, p3): # Finner avstanden fra linjen mellom to punkter (et element) til et punkt (angrepspunkt)
        return np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
    
    def fibPair(self, pair):                                                 # Finner fastinnspenningsmoment for endepunktene til et element
        if not pair[0].distLoad:    
            P = pair[0].intencity                                      # Intensitet på lasten
            phi = pair[0].angle - pair[1].angle                        # Lastens vinkel på alement
            a = np.linalg.norm(pair[0].attackPoint - pair[1].P1.punkt) # Avtand fra last til P1
            b = np.linalg.norm(pair[0].attackPoint - pair[1].P2.punkt) # Avstand fra last til P2
            L = pair[1].lenElem                                        # Elementlengde
            M1 = -(P * np.sin(phi) * a * b**2)/L                       # Fast innspenningsmoment i P1 (Globalt knutepunkt nr. index1)
            M2 = (P * np.sin(phi) * a**2 * b)/L
            q1 = M1 + M2 + P  * a
            q2 = P - q1
        else:
            phi = pair[0].angle - pair[1].angle
            p = pair[0].intencity * np.sin(phi) # Ser bare på kreftene normalt på elementene
            L = pair[1].L 
            a = np.linalg.norm(pair[0].startPoint - pair[1].P1.punkt) # Avtand fra last til P1
            b = L - np.linalg.norm(pair[0].endPoint - pair[1].P1.punkt)
            s = np.linalg.norm(pair[0].startPoint - pair[0].endPoint)
            if pair[0].type == 0:
                M1 = -((s+a)**2 * (6*b**2+4*b*(s+a)+(s+a)**2) + s**2*(6*(s+b)**2+4*a*(s+b)+a**2))*p/(12*L**2)
                M2 = ((s+b)**2 * (6*a**2+4*a*(s+b)+(s+b)**2) + s**2*(6*(s+a)**2+4*b*(s+a)+b**2))*p/(12*L**2)
                q1 = (M1 + M2 + s*p*(s/2+b))/L
                q2 = s * p - q1
            elif pair[0].type == 1:
                M1 = -(p*s**3)/(60*L)*(5-3*s/L)
                M2 = (p*s**2)/(60) * (10 - 10*s/L + 3*s**2/L**2)
                q1 = (M1 + M2 + s**2/6)/L
                q2 = s * p/2 - q1
            elif pair[0].type == 2:
                M1 = -(p*s**2)/(60) * (10 - 10*s/L + 3*s**2/L**2)
                M2 = (p*s**3)/(60*L)*(5-3*s/L)
                q2 = (M1 + M2 + s**2/6)/L
                q1 = s * p/2 - q2
            elif pair[0].type == 3:
                M1 = -(p*s**2)/(30) * (10 - 15*s/L + 6*s**2/L**2)
                M2 = (p*s**3)/(20*L)*(L-4*b/L)
                q2 = (M1 + M2 + s**2/3)/L
                q1 = s * p/2 - q2
            elif pair[0].type == 4:
                M1 = -(p*s**3)/(20*L)*(L-4*a/L)
                M2 = (p*s**2)/(30) * (10 - 15*s/L + 6*s**2/L**2)
                q1 = (M1 + M2 + s**2/3)/L
                q2 = s * p/2 - q1
            elif pair[0].type == 5:
                M1 = -13/192 * p*L**2
                M2 = 13/192 * p*L**2
                q1 = p*L/3
                q2 = q1
            else:
                M1 = -2/(np.pi)**3 * p*L**2
                M2 = 2/(np.pi)**3 * p*L**2
                q1 = p/(np.pi * 2* L)
                q2 = q1
        return [0, q1, M1, 0, q2, M2]

    def __init__(self, lastOb, elemOb, npunkt, nelem):
        self.fib = np.zeros(npunkt*3)   # Systemlastvektor med fast innspenningsmoment og last.
        self.pairs = []

        for i in range(len(lastOb)):    # Ønsker å sjekke om en last virker på et elemnt, for så å legge inn par i 'pairs'.
            if not lastOb[0].distLoad:  # Hvis ikke fordelt last
                for j in range(nelem):
                    d = self.dist(elemOb[j].P1.punkt, elemOb[j].P2.punkt, lastOb[i].attackPoint)    # Avstand fra angrepspunkt til element
                    if d < 0.01:        # Hvis angrepspunktet er på elementet
                        self.pairs.append((lastOb[i], elemOb[j]))
            else:
                for j in range(nelem): 
                    d1 = self.dist(elemOb[j].P1.punkt, elemOb[j].P2.punkt, lastOb[i].startPoint)    # Avstand fra startpunkt til element
                    d2 = self.dist(elemOb[j].P1.punkt, elemOb[j].P2.punkt, lastOb[i].endPoint)      # Avstand fra sluttpunkt til element
                    if d1 + d2 < 0.02:  # Hvis begge punkt ligger på elementet
                        self.pairs.append((lastOb[i], elemOb[j]))

        for pair in self.pairs:
            s = self.fibPair(pair)
            s = pair[1].transformToGlobal(pair[1].angle, s)
            index1R = 3*pair[1].P1.punktn + 1           # Index moment i ende 1 i Systemlastvektor-vektor
            index2R = 3*pair[1].P2.punktn + 1           # Index for moment i ende to i Systemlastvektor
            self.fib[index1R + 1] -= s[2]               # Fast innspenningsmoment i P1 (Globalt knutepunkt nr. index1)
            self.fib[index1R ] -= s[1]                  # Fast innspenningslast i P1
            self.fib[index2R + 1] -= s[5]               # Fast innspenningsmoment i P2 (Globalt knutepunkt nr. index2)
            self.fib[index2R] -= s[4]                   # Fast innspenningslast i P2

    