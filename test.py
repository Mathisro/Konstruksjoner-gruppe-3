from structureVisualization import *
import numpy as np
import Punkt
import Last
import Element
import lesinput
import FastInnMom
import SysStiMat
import Tverrsnitt
import EndeMom
import Diagrammer
import Kapasitet

npunkt = 2
punkt = np.array([np.array([0, 0, (1, 1, 0)], dtype=object), np.array([0, 1, (1, 1, 0)], dtype=object)], dtype=object) # Punkter på formen: (x, y, (innspenning x, innspenning y, momentinnspenning))
nelem = 1
elem = np.array([np.array([0, 0, 1, 1, 350])]) # Elementer på formen [elementnummer, globalt punkt 1, globalt punkt 2, tverrsnittype, flytspenning]
nlast = 1
last = np.array([np.array([0, 0, 0.5, 1, 0, 0, 1])])#, np.array([1, 0, np.array([0.5, 0]), 0, -90])], dtype=object)
# Last: [(Type last: 0 = punktlast,  1 = jevnt fordelt, 2 = trekant maks til høyre ytterst, 3 = trekant m/ maks venstre ytterst
# 4 = trekant venstre maks innerst, 5 = trekant høyre maks innesrt , 6 = parabel, 7 = sinus), 
# x1, y1, x2, y2, vinkel i grader, intensitet]
tverrsnitt = np.array([np.array([1, 0.2, 0, 0.2, 0, 0, 0, 0, 0, 1, 21000])])
# [Index, H, h, B, b, R, r, T_stag, T_flens, Matr_type, E_modul]

# -----Rammeanalyse-----
def main_test():
    
    # Plotter figurer
    # 
    
    fig_init, ax_init, fig_def, ax_def = setup_plots()  # Initialiserer figurer til visualiseringen
    first_index = 0 # Første index brukt

    npunkt, punkt, nelem, elem, nlast, last, tverrsnitt = lesinput.lesinput('Inputfil-endelig.csv') # Leser input-data

    punkt = np.array(punkt)
    elem = np.array(elem)
    tverrsnitt = np.array(tverrsnitt)

    

    plot_structure(ax_init, punkt, elem, 1, first_index) # Plotter initalramme
 
    # Regner ut lengder til elementene
    # elementlengder = lengder(punkt, elem, nelem) ## Gjøres i hvert objekt

    # Initialiserer liste med alle objektene
    
    tverrsnittOb = []
    for tsnitt in tverrsnitt:
        tverrsnittOb.append(Tverrsnitt.Tverrsnitt(tsnitt))

    punktOb = []
    for i in range(npunkt):
        punktOb.append(Punkt.Punkt(i, punkt[i]))
        
    elementOb = []
    for i in range(nelem):
        elementOb.append(Element.Element(i, elem[i], punktOb, tverrsnittOb))

    lastOb = []
    for i in range(nlast):
        lastOb.append(Last.Last(i, last[i]))

    print(len(lastOb))
 
    # -----Fastinnspenningsmomentene------
    # Lag funksjonen selv
    fim = FastInnMom.FastInnMom(lastOb, elementOb, npunkt, nelem)
 
    # -----Setter opp lastvektor-----
    # Lag funksjonen selv
    b = fim.fib

    print(b)
 
    # ------Setter opp systemstivhetsmatrisen-----
    # Lag funksjonen selv
    K = SysStiMat.SysStiMat(elementOb, npunkt, punktOb)
 
    # ------Innfører randbetingelser------
    # Lag funksjonen selv
    K.randBet(punktOb, npunkt)

    print(K.K)
 
    # -----Løser ligningssystemet------
    # Lag funksjonen selv
    rot = np.linalg.solve(K.K, b)
    # Hint, se side for løsing av lineære systemer i Python
     
    #------Finner endemoment for hvert element-----
    # Lag funksjonen selv
    endemoment = EndeMom.EndeMom(elementOb, rot, fim).endeMom

    #print(endemoment)
 
    #-----Skriver ut hva rotasjonen ble i de forskjellige nodene-----
    print("Rotasjoner i de ulike punktene:")
    print(rot)
 
    #-----Skriver ut hva momentene ble for de forskjellige elementene-----
    print("Elementvis endemoment:")
    print(endemoment)
    
    
 
    #-----Plott deformert ramme-----
    scaleRot = 10 # Du kan endre denne konstanten for å skalere de synlige deformasjonene til rammen
    scaleTrans = 10
    plot_structure_def(ax_def, punkt, elem, 1, first_index, rot, scaleRot, scaleTrans)
  
    
    Diagrammer.Diagrammer(elementOb, endemoment, nelem)
    
    kap = Kapasitet.Kapasitet(elementOb)

    print(kap.kapasitet)

    for i, kp in enumerate(kap.kapasitet):
        print(f'Bjelke: {elementOb[i].elem_n}, Tverrsnitt: {elementOb[i].tSnitt.type}, Kapasitet: {kp}')

    plt.show()

    

main_test()