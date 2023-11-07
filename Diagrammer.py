import matplotlib.pyplot as plt
import numpy as np

class Diagrammer:
    
    def diagram(self, mom, elem, x):
        M1 = mom[elem.elem_n, 2]
        Q1 = mom[elem.elem_n, 1]
        N1 = mom[elem.elem_n, 0]

        M, V, N = np.zeros(len(x)), np.zeros(len(x)), np.zeros(len(x))        

        if elem.harLast():
            for last in elem.last:

                phi = -last.angle + elem.angle                         # Intensitet på lasten
                P = last.intencity * np.sin(phi) 

                if not last.distLoad:
                    a = np.linalg.norm(last.attackPoint - elem.P1.punkt)

                    xFirstPart = x[:int(a/elem.L * len(x))]
                    xSecondPart = x[int(a/elem.L * len(x)):]

                    M_1 = list(np.zeros(len(xFirstPart)))
                    M_2 = list(P*(xSecondPart - a))

                    Q_1 = list(np.zeros(len(xFirstPart)))
                    Q_2 = list(np.zeros(len(xSecondPart)) + P)

                    M += np.array(M_1 + M_2)
                    V += np.array(Q_1 + Q_2)

                elif last.type == 1:
                    M += P*x*x/2
                    V += P*x

                else:
                    M += (P*x**2)/(6*elem.L)
                    V += (P*x)/(2*elem.L)            
        
        M += -M1 - Q1*x
        V += -Q1 + np.zeros(len(x))
        N += -N1 + np.zeros(len(x))
        return M, V, N


    def plotSubplot(self, i, x, y, tittel):
        plt.subplot(self.n_rows, 3, i+1)
        plt.plot(x, y)
        plt.plot(x, np.zeros(len(x)))
        plt.title(tittel)

    def __init__(self, elemOb, endeMom, elem_n):
        self.n = elem_n
        self.n_rows = self.n // 3 + 1

        M, V, N = [], [], []

        for elem in elemOb:
            x = np.linspace(0, elem.L, 1000)
            m, v, n = self.diagram(endeMom, elem, x)

            M.append(m)
            V.append(v)
            N.append(n)

            elem.M = m
            elem.V = v
            elem.N = n

        # Plotter M-Diagrammer
        plt.figure(figsize=(15, 5 * self.n_rows))
        plt.suptitle('M-DIagram [Nm]', fontsize=16)

        for i in range(elem_n):
            self.plotSubplot(i, x, M[i], f'Bjelke {i}')

        # Plotter V-Diagrammer
        plt.figure(figsize=(15, 5 * self.n_rows))
        plt.suptitle('V-diagram [N]', fontsize=16)

        for i in range(elem_n):
            self.plotSubplot(i, x, V[i], f'Bjelke {i}')

        # Plotter N-Diagrammer
        plt.figure(figsize=(15, 5 * self.n_rows))
        plt.suptitle('N-diagram [N]', fontsize=16)

        for i in range(elem_n):
            self.plotSubplot(i, x, N[i], f'Bjelke {i}')
