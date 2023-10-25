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

npunkt = 2
punkt = np.array([np.array([0, 0, (1, 1, 0)]),np.array([1, 0, (1, 0, 0)])], dtype=object) # Punkter på formen: (x, y, (innspenning x, innspenning y, momentinnspenning))
nelem = 1
elem = np.array([np.array([0, 1, 1])]) # Elementer på formen [globalt punkt 1, globalt punkt 2, tverrsnittype]
nlast = 2
last = np.array([np.array([2, 1, np.array([0, 0]), np.array([1, 0]), -90]), np.array([1, 0, np.array([0.5, 0]), 0, -90])], dtype=object)
# Last: [(Type last: 1 = punktlast,  2 = jevnt fordelt, 3 = trekant maks til høyre ytterst, 4 = trekant m/ maks venstre ytterst
# 5 = trekant venstre maks innerst, 6 = trekant høyre maks innesrt , 7 = parabel, 8 = sinus), 
# intenistet, startpunkt, sluttpunnkt, retning i grader, type fordelt: ]
tverrsnitt = np.array([np.array([0, 1, 0, 12, 0, 0, 0, 0, 0, 1, 1])])
# [Index, H, h, B, b, R, r, T_stag, T_flens, Matr_type, E_modul]

# -----Rammeanalyse-----
def main_test():
    
    # Plotter figurer
    # 
    
    fig_init, ax_init, fig_def, ax_def = setup_plots()  # Initialiserer figurer til visualiseringen
    first_index = 0 # Første index brukt

    npunkt, punkt, nelem, elem, nlast, last, tverrsnitt = lesinput.lesinput('Inputfil_portal.csv') # Leser input-data
 
    plot_structure(ax_init, punkt, elem, 1, first_index) # Plotter initalramme
 
    # Regner ut lengder til elementene
    # elementlengder = lengder(punkt, elem, nelem) ## Gjøres i hvert objekt

    # Initialiserer liste med alle objektene
    
    tverrsnittOb = []
    for i in range(len(tverrsnitt)):
        tverrsnittOb.append(Tverrsnitt.Tverrsnitt(tverrsnitt[i]))

    punktOb = []
    for i in range(npunkt):
        punktOb.append(Punkt.Punkt(i, punkt[i]))
        
    elementOb = []
    for i in range(nelem):
        elementOb.append(Element.Element(i, elem[i], punktOb, tverrsnittOb))

    lastOb = []
    for i in range(nlast):
        lastOb.append(Last.Last(i, last[i]))
 
    # -----Fastinnspenningsmomentene------
    # Lag funksjonen selv
    fim = FastInnMom.FastInnMom(lastOb, elementOb, npunkt, nelem)
 
    # -----Setter opp lastvektor-----
    # Lag funksjonen selv
    b = fim.fib

    #print(b)
 
    # ------Setter opp systemstivhetsmatrisen-----
    # Lag funksjonen selv
    K = SysStiMat.SysStiMat(elementOb, nelem)
 
    # ------Innfører randbetingelser------
    # Lag funksjonen selv
    K.randBet(elementOb)

    #print(K.K)
 
    # -----Løser ligningssystemet------
    # Lag funksjonen selv
    rot = np.linalg.solve(K.K, b)
    print(rot)
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
    #print(endemoment)

    rot = [rot[2], rot[5]]
 
    #-----Plott deformert ramme-----
    skalering = 100;     # Du kan endre denne konstanten for å skalere de synlige deformasjonene til rammen
    plot_structure_def(ax_def, punkt, elem, 1, first_index, skalering*rot)
    plt.show()

main_test()