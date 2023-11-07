import numpy as np


class EndeMom:

    def __init__(self, elemOb, rot):                        # Initialiserer klassen
        self.endeMom = []

        for elem in elemOb:                                 # Itererer gjennom elementene for å regne ut endereaksjonene
            V_that = []

            for i in range (6):
                V_that.append(rot[elem.indexFromKtab(i)])   # Finner deformasjonene for endepunktene

            V = np.array(elem.transformFromGlobal(V_that))  # Transformerer deformsajonsvektoren til lokalt system

            S = np.matmul(elem.k, V) + elem.fastInnMom      # Løser S = Kv + S_fast

            self.endeMom.append(S)                          # Legger til i liste for alle element
            
        self.endeMom = np.array(self.endeMom)

