import numpy as np


class EndeMom:

    def __init__(self, elemOb, rot, fim):
        self.endeMom = []

        for elem in elemOb:
            V_that = []
            S_that = []

            for i in range (6):
                V_that.append(rot[elem.indexFromKtab(i)])
                S_that.append(fim.fib[elem.indexFromKtab(i)])

            V_that = np.array(elem.transformFromGlobal(V_that))
            S_that = np.array(elem.transformFromGlobal(S_that))

            S = np.matmul(elem.k, V_that) + S_that

            self.endeMom.append(S)
            
        self.endeMom = np.array(self.endeMom)

