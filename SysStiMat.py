import numpy as np

class SysStiMat:

    def __init__(self, elemOb, n):                  # Initialiserer objektet
        self.K = np.zeros((n*3)**2)
        self.K = np.reshape(self.K, (n*3, n*3))     # Lager matrisen med riktig størrelse

        for elem in elemOb:                         # Itererer gjennom objektene
            Khat = elem.transformKToGlobal()        # Elementstivhetsmatrise i globalt system

            for i in range(6):
                for j in range(6):                  # Adderer inn bidragene på rett plass
                    self.K[elem.indexFromKtab(i), elem.indexFromKtab(j)] += Khat[i, j]  

    def randBet(self, punktOb, n):

        for i in range(n):

            for j in range(3):
                b = punktOb[i].boundryVal[j]        # Henter punktets randbetingelser

                if b:
                    index = 3*i + j                 # Index for frihetsgrad j for punkt i
                    self.K[index, index] *= 10e9    # Ganger opp til kunstig høy stivhet på diagonalen

 