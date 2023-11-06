import numpy as np

class SysStiMat:

    def __init__(self, elemOb, n, punktOb):
        self.K = np.zeros((n*3)**2)
        self.K = np.reshape(self.K, (n*3, n*3))

        for elem in elemOb:
            Khat = elem.transformKToGlobal()

            for i in range(6):
                for j in range(6):
                    self.K[elem.indexFromKtab(i), elem.indexFromKtab(j)] += Khat[i, j]

    def randBet(self, punktOb, n):

        for i in range(n):

            for j in range(3):
                b = punktOb[i].boundryVal[j]

                if b:
                    index = 3*i + j
                    self.K[index, index] *= 10e9

 