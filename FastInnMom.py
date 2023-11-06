import numpy as np

class FastInnMom:

    def dist(self, p1, p2, p3): # Finner avstanden fra linjen mellom to punkter (et element) til et punkt (angrepspunkt)
        return np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
    
    def isBetween(self, a, b, p):
        x1, y1 = a
        x2, y2 = b
        x0, y0 = p
        
        is_x_between = (x1 <= x0 <= x2) or (x2 <= x0 <= x1)
        is_y_between = (y1 <= y0 <= y2) or (y2 <= y0 <= y1)
        
        return is_x_between and is_y_between
    
    def fastInnKrefter(self, elem):
        M1, M2, q1, q2 = 0, 0, 0, 0

        for last in elem.last: 
            print(last.lastn)                            # Finner fastinnspenningsmoment for endepunktene til et element
            if not last.distLoad:                                      
                phi = -last.angle + elem.angle                         # Intensitet på lasten
                p = last.intencity * np.sin(phi)                     # Lastens vinkel på alement
                a = np.linalg.norm(last.attackPoint - elem.P1.punkt) # Avtand fra last til P1
                b = np.linalg.norm(last.attackPoint - elem.P2.punkt) # Avstand fra last til P2
                L = elem.L                                        # Elementlengde

                M1 += -(p * a * b**2)/L                       # Fast innspenningsmoment i P1 (Globalt knutepunkt nr. index1)
                M2 += (p * a**2 * b)/L
                q1 += -(-M1 - M2 + p  * b)/L        # FINNE UT AV MINUSEN HER!!!
                q2 += p - q1

            else:
                phi = -last.angle + elem.angle
                p = last.intencity * np.sin(phi) # Ser bare på kreftene normalt på elementene
                L = elem.L 
                a = np.linalg.norm(last.startPoint - elem.P1.punkt) # Avtand fra last til P1
                b = L - np.linalg.norm(last.endPoint - elem.P1.punkt)
                s = np.linalg.norm(last.startPoint - last.endPoint)
                #print(p)

                if last.type == 1:
                    M1 += -((s+a)**2 * (6*b**2+4*b*(s+a)+(s+a)**2) + s**2*(6*(s+b)**2+4*a*(s+b)+a**2))*p/(12*L**2)
                    M2 += ((s+b)**2 * (6*a**2+4*a*(s+b)+(s+b)**2) + s**2*(6*(s+a)**2+4*b*(s+a)+b**2))*p/(12*L**2)
                    q1 += (-M1 - M2 + s*p*(s/2+b))/L
                    q2 += s * p - q1

                elif last.type == 2:
                    M1 += -(p*s**3)/(60*L)*(5-3*s/L)
                    M2 += (p*s**2)/(60) * (10 - 10*s/L + 3*s**2/L**2)
                    q1 += (-M1 + M2 + s**2/6)/L
                    q2 += s * p/2 - q1

                elif last.type == 3:
                    M1 += -(p*s**2)/(60) * (10 - 10*s/L + 3*s**2/L**2)
                    M2 += (p*s**3)/(60*L)*(5-3*s/L)
                    q2 += (M1 + M2 + s**2/6)/L
                    q1 += s * p/2 - q2

                elif last.type == 4:
                    M1 += -(p*s**2)/(30) * (10 - 15*s/L + 6*s**2/L**2)
                    M2 += (p*s**3)/(20*L)*(L-4*b/L)
                    q2 += (M1 + M2 + s**2/3)/L
                    q1 += s * p/2 - q2

                elif last.type == 5:
                    M1 += -(p*s**3)/(20*L)*(L-4*a/L)
                    M2 += (p*s**2)/(30) * (10 - 15*s/L + 6*s**2/L**2)
                    q1 += (M1 + M2 + s**2/3)/L
                    q2 += s * p/2 - q1

                elif last.type == 6:
                    M1 += -13/192 * p*L**2
                    M2 += 13/192 * p*L**2
                    q1 += p*L/3
                    q2 += q1

                else:
                    M1 += -2/(np.pi)**3 * p*L**2
                    M2 += 2/(np.pi)**3 * p*L**2
                    q1 += p/(np.pi * 2* L)
                    q2 += q1

        return [0, q1, M1, 0, q2, M2]

    def __init__(self, lastOb, elemOb, npunkt, nelem):
        self.fib = np.zeros(npunkt * 3)

        for i in range(len(lastOb)):    # Ønsker å sjekke om en last virker på et elemnt, for så å legge inn par i 'pairs'.
            if not lastOb[i].distLoad:  # Hvis ikke fordelt last
                for j in range(nelem):
                    P1, P2 = elemOb[j].P1.punkt, elemOb[j].P2.punkt
                    A = lastOb[i].attackPoint

                    d = self.dist(P1, P2, A)    # Avstand fra angrepspunkt til element
                    between = self.isBetween(P1, P2, A)

                    if abs(d) < 0.01 and between:        # Hvis angrepspunktet er på elementet
                        elemOb[j].last.append(lastOb[i])
                        # print(elemOb[j].elem_n)
                        # print(lastOb[i].lastn)

            else:
                for j in range(nelem): 
                    P1, P2 = elemOb[j].P1.punkt, elemOb[j].P2.punkt
                    S1, S2 = lastOb[i].startPoint, lastOb[i].endPoint
                    
                    d1 = self.dist(P1, P2, S1)    # Avstand fra startpunkt til element
                    d2 = self.dist(P1, P2, S2)      # Avstand fra sluttpunkt til element
                    between = (self.isBetween(P1, P2, S1) and
                               self.isBetween(P1, P2, S2)     )
                    
                    if np.abs(d1 + d2) < 0.02 and between:  # Hvis begge punkt ligger på elementet
                        elemOb[j].last.append(lastOb[i])
                        # print(elemOb[j].elem_n)
                        # print(lastOb[i].lastn)

        # for pair in self.pairs:
        #     elem = elem
        #     print(f'Elementnummer: {elem.elem_n}, lastnummer: {last.lastn}')
        #     s = elem.transformToGlobal(self.fibPair(pair))

        #     for i in range(6):
        #         self.fib[elem.indexFromKtab(i)] += s[i]

        for elem in elemOb:
            if elem.harLast():
                s = elem.transformToGlobal(self.fastInnKrefter(elem))

                for i in range(6):
                    self.fib[elem.indexFromKtab(i)] += s[i]


    