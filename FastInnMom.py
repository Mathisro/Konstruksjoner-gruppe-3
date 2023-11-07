import numpy as np

class FastInnMom:

    def dist(self, p1, p2, p3):                                 # Finner avstanden fra linjen mellom to punkter til et punkt
        return np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
    
    def isBetween(self, p1, p2, p3):                            # Sjekker om et punkt er mellom to andre
        x1, y1 = p1
        x2, y2 = p2
        x0, y0 = p3
        
        is_x_between = (x1 <= x0 <= x2) or (x2 <= x0 <= x1)
        is_y_between = (y1 <= y0 <= y2) or (y2 <= y0 <= y1)
        
        return is_x_between and is_y_between
    
    def fastInnKrefter(self, elem):                                  # Regner ut fastinnspenningskrefter
        M1, M2, q1, q2 = 0, 0, 0, 0

        for last in elem.last:                                       # Finner finner krefter for hver ytre last
            if not last.distLoad:                                    # Hvis punktlast

                phi = -last.angle + elem.angle                       # Lastens vinkel på i forhold til element
                p = last.intencity * np.sin(phi)                     # Ser bare på kreftene normalt på elementene
                a = np.linalg.norm(last.attackPoint - elem.P1.punkt) # Avtand fra last til P1
                b = np.linalg.norm(last.attackPoint - elem.P2.punkt) # Avstand fra last til P2
                L = elem.L                                           # Elementlengde

                M1 += -(p * a * b**2)/L**2                           # Fast innspenningsmoment fra tabell 8.3 i kompendiet
                M2 += (p * a**2 * b)/L**2
                q = (-M1 - M2 + p  * b)/L                            # Momentlikevekt
                q2 += p - q
                q1 += q

            else:                                                    # Fordelt last
                phi = -last.angle + elem.angle
                p = last.intencity * np.sin(phi)                     # Ser bare på kreftene normalt på elementene
                L = elem.L 

                a = np.linalg.norm(last.startPoint - elem.P1.punkt)
                b = L - np.linalg.norm(last.endPoint - elem.P1.punkt)
                s = np.linalg.norm(last.startPoint - last.endPoint)  # Lengde på last

                if last.type == 1:  # Jevnt fordelt last
                    M1 += -(p*(s+a)**2)/(12*L**2)*(6*b**2 + 4*b*(s+a) + (s+a)**2) + (p*a**2)/(12*L**2)*(6*(s+b)**2 + 4*(s+b)+a**2) # Fra tab. 8.3 og superposison
                    M2 += (p*(s+a)**2)/(12*L**2) * (4*b + s + a) - (p*a**3)/(12*L**2) * (4*(s+b) + a)
                    q = (-M1 - M2 + s*p*(s/2+b))/L
                    q2 += s * p - q
                    q1 += q


                elif last.type == 2:                                    # Trekantlast med maks ytterst til høyre
                    M1 += -(p*s**3)/(60*L)*(5-3*s/L)                    # Fra tabell 8.3
                    M2 += (p*s**2)/(60) * (10 - 10*s/L + 3*s**2/L**2)

                    q = (-M1 - M2 + s**2/6)/L
                    q2 += s * p/2 - q
                    q1 += q

                elif last.type == 3:                                    # Trekantlast med maks ytterst til venstre
                    M1 += -(p*s**2)/(60) * (10 - 10*s/L + 3*s**2/L**2)  # Fra tabell 8.3
                    M2 += (p*s**3)/(60*L)*(5-3*s/L)
                    q2 += (M1 + M2 + s**2/6)/L
                    q1 += s * p/2 - q2

                elif last.type == 4:                                    # Trekantlast med maks innerst til høyre
                    M1 += -(p*s**2)/(30) * (10 - 15*s/L + 6*s**2/L**2)  # Tra tabell 8.3
                    M2 += (p*s**3)/(20*L)*(L-4*b/L)
                    q2 += (M1 + M2 + s**2/3)/L
                    q1 += s * p/2 - q2

                elif last.type == 5:                                    # Trekantlast med maks innerst til venstre
                    M1 += -(p*s**3)/(20*L)*(L-4*a/L)                    # Fra tabell 8.4
                    M2 += (p*s**2)/(30) * (10 - 15*s/L + 6*s**2/L**2)
                    q1 += (M1 + M2 + s**2/3)/L
                    q2 += s * p/2 - q1

                elif last.type == 6:                                    # Parabellast
                    M1 += -13/192 * p*L**2                              # Fra tab. 8.3
                    M2 += 13/192 * p*L**2
                    q1 += p*L/3
                    q2 += q1

                else:                                                   # Sinuslast
                    M1 += -2/(np.pi)**3 * p*L**2                        # Fra tab. 8.3
                    M2 += 2/(np.pi)**3 * p*L**2
                    q1 += p/(np.pi * 2* L)
                    q2 += q1

        return np.array([0, q1, M1, 0, q2, M2])                         # Returnerer lokal lastvektor
    
    def finnLaster(self, lastOb, elemOb, nelem):

        for i in range(len(lastOb)):                                    # Ønsker å sjekke om en last virker på et element
            if not lastOb[i].distLoad:                                  # Punktlast
                for j in range(nelem):

                    P1, P2 = elemOb[j].P1.punkt, elemOb[j].P2.punkt
                    A = lastOb[i].attackPoint

                    d = self.dist(P1, P2, A)                            # Avstand fra angrepspunkt til element
                    between = self.isBetween(P1, P2, A)                 # Elementet ligger mellom punktene

                    if abs(d) < 0.01 and between:                       # Hvis angrepspunktet er på elementet
                        elemOb[j].last.append(lastOb[i])


            else:
                for j in range(nelem):                                  # Hvis fordelt last

                    P1, P2 = elemOb[j].P1.punkt, elemOb[j].P2.punkt  
                    S1, S2 = lastOb[i].startPoint, lastOb[i].endPoint
                    
                    d1 = self.dist(P1, P2, S1)                          # Avstand fra startpunkt til element
                    d2 = self.dist(P1, P2, S2)                          # Avstand fra sluttpunkt til element
                    between = (self.isBetween(P1, P2, S1) and
                               self.isBetween(P1, P2, S2)     )         # Begge punktene ligger mellom endepuntktene
                    
                    if np.abs(d1 + d2) < 0.02 and between:              # Hvis begge punkt ligger på elementet
                        elemOb[j].last.append(lastOb[i])


    def __init__(self, lastOb, elemOb, npunkt, nelem):                  # Initialisrer objektet
        
        self.fib = np.zeros(npunkt * 3)

        self.finnLaster(lastOb, elemOb, nelem)                          # Legger lastene til i elementobjektene

        for elem in elemOb:
            if elem.harLast():
                s = self.fastInnKrefter(elem)                           # Elementets fastinnspenningreaksjoner
                sThat = elem.transformToGlobal(s)                       # Transformerer til globalt system

                elem.fastInnMom = s                                     # Legger fastinnspenningsreaksjonene til i elementet

                for i in range(6):
                    self.fib[elem.indexFromKtab(i)] -= sThat[i]         # Adderer inn med negativt fortegn på riktig plass i global lastvektor


    