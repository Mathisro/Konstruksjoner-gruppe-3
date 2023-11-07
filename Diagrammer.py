import matplotlib.pyplot as plt
import numpy as np

class Diagrammer:
    
    def diagram(self, mom, elem, x):                                    # Finner funksjoner for diagrammer ved snittmetoden
        M1 = mom[elem.elem_n, 2]                                        # Endemoment
        Q1 = mom[elem.elem_n, 1]                                        # Ende-skjærkraft
        N1 = mom[elem.elem_n, 0]                                        # Ende-aksialkraft

        M, V, N = np.zeros(len(x)), np.zeros(len(x)), np.zeros(len(x))  

        if elem.harLast():                                              # Sjekker om elemetet har ytre last
            for last in elem.last:                                      # Finner bidrag fra hver kraft

                phi = -last.angle + elem.angle                          # Vinkel for intensitet normalt på bjelken
                P = last.intencity * np.sin(phi) 

                if not last.distLoad:                                   # I tilfelle punktlast
                    a = np.linalg.norm(last.attackPoint - elem.P1.punkt)

                    xFirstPart = x[:int(a/elem.L * len(x))]             # Deler x-verdiene ved lasten
                    xSecondPart = x[int(a/elem.L * len(x)):]

                    M_1 = list(np.zeros(len(xFirstPart)))               # Bruker list() for å lett kunne addere sammen de to delene
                    M_2 = list(P*(xSecondPart - a))                     # Kun bidrag etter lastens angrepspunkt

                    Q_1 = list(np.zeros(len(xFirstPart)))
                    Q_2 = list(np.zeros(len(xSecondPart)) + P)          # Kun bidrag etter lastens angrepspunkt

                    M += np.array(M_1 + M_2)                            # Setter sammen de to delene og legger til bidraget fra lasten
                    V += np.array(Q_1 + Q_2)

                elif last.type == 1:                                    # Hvis jevnt fordelt last
                    M += P*x*x/2                                        # Snittmetoden
                    V += P*x

                else:                                                   # Hvis trekantlast
                    M += (P*x**2)/(6*elem.L)                            # Snittmetoden
                    V += (P*x)/(2*elem.L)            
        
        M += -M1 - Q1*x                                                 # Adderer inn bidrag fra endemoment
        V += -Q1 + np.zeros(len(x))
        N += -N1 + np.zeros(len(x))
        return M, V, N


    def plotSubplot(self, i, x, y, tittel):                             # Oppretter plott
        plt.subplot(self.n_rows, 5, i+1)                                # Plotter på riktig posisjon i figuren
        plt.plot(x, y)
        plt.plot(x, np.zeros(len(x)))
        plt.title(tittel)

    def __init__(self, elemOb, endeMom, elem_n):                        # Initialiserer klassen
        self.n = elem_n
        self.n_rows = self.n // 5 + 1                                   # Antall rader i figuren

        M, V, N = [], [], []

        for elem in elemOb:                                             # Itererer gjennom elementene of finner diagrammene
            x = np.linspace(0, elem.L, 1000)
            m, v, n = self.diagram(endeMom, elem, x)

            M.append(m)
            V.append(v)
            N.append(n)

            elem.M = m
            elem.V = v
            elem.N = n

        # Plotter M-Diagrammer
        plt.figure(figsize=(15, 5 * self.n_rows))                       # Figur for M-diagrammer
        plt.suptitle('M-Diagram [Nm]', fontsize=16)
        plt.subplots_adjust(wspace=0.5, hspace=0.5)

        for i in range(elem_n):
            self.plotSubplot(i, x, M[i], i)                             # Fyller ut figuren

        # Plotter V-Diagrammer
        plt.figure(figsize=(15, 5 * self.n_rows))                       # Figur for V-diagrammer
        plt.suptitle('V-diagram [N]', fontsize=16)
        plt.subplots_adjust(wspace=0.5, hspace=0.5)

        for i in range(elem_n):
            self.plotSubplot(i, x, V[i], i)                             # Fyller ut figuren

        # Plotter N-Diagrammer
        plt.figure(figsize=(15, 5 * self.n_rows))                       # Figur for N-diagrammer
        plt.suptitle('N-diagram [N]', fontsize=16)
        plt.subplots_adjust(wspace=0.5, hspace=0.5)

        for i in range(elem_n):
            self.plotSubplot(i, x, N[i], i)                             # Fyller ut figuren
