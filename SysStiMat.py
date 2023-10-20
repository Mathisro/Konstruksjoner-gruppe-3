import numpy as np

class SysStiMat:

    def __init__(self, elemOb, n):
        self.K = np.zeros((n*6)**2)
        self.K = np.reshape(self.K, (n*6, n*6))

        for elem in elemOb:
            k = elem.k
            Khat = elem.transformKToGlobal
            kTab = elem.kTab

            for i in range(6):
                for j in range(6):
                    self.K[kTab[:, 2][i], kTab[:, 2][j]] = k[i, j]

    def randBet(self, elemOb):

        for elem in elemOb:
            boundryVal = elem.P1.boundryVal

            b1, b2, b3 = boundryVal[0], boundryVal[1], boundryVal[2]

            index1 = elem.kTab[0, 2]
            index2 = elem.kTab[1, 2]
            index3 = elem.kTab[2, 2]

            self.K[index1, index1] *= 10e6 * b2
            self.K[index2, index2] *= 10e6 * b1
            self.K[index3, index3] *= 10e6 * b3

            boundryVal = elem.P2.boundryVal

            b1, b2, b3 = boundryVal[0], boundryVal[1], boundryVal[2]

            index1 = elem.kTab[3, 2]
            index2 = elem.kTab[4, 2]
            index3 = elem.kTab[5, 2]

            self.K[index1, index1] *= 10e6 * b2
            self.K[index2, index2] *= 10e6 * b1
            self.K[index3, index3] *= 10e6 * b3

            
 