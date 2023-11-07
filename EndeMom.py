import numpy as np


class EndeMom:

    def __init__(self, elemOb, rot, fim):
        self.endeMom = []

        for elem in elemOb:
            V_that = []

            for i in range (6):
                V_that.append(rot[elem.indexFromKtab(i)])

            V = np.array(elem.transformFromGlobal(V_that))

            S = np.matmul(elem.k, V) + elem.fastInnMom

            self.endeMom.append(S)
            
        self.endeMom = np.array(self.endeMom)

