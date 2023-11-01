import numpy as np

class SysStiMat:

    def __init__(self, elemOb, n):
        self.K = np.zeros((n*3)**2)
        self.K = np.reshape(self.K, (n*3, n*3))

        for elem in elemOb:
            Khat = elem.transformKToGlobal()

            for i in range(6):
                for j in range(6):
                    self.K[elem.indexFromKtab(i), elem.indexFromKtab(j)] += Khat[i, j]

    def randBet(self, elemOb):

        for elem in elemOb:

            for i in range(3):
                b1 = elem.P1.boundryVal[i]
                b2 = elem.P2.boundryVal[i]

                if b1:
                    index = elem.indexFromKtab(i)
                    self.K[index, index] *= 10e9

                if b2:
                    index = elem.indexFromKtab(i + 3)
                    self.K[index, index] *= 10e9

 