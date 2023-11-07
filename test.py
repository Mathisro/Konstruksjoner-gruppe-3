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
    
    #-----Klargjør for plotting med utdelt kode-----
    fig_init, ax_init, fig_def, ax_def = setup_plots()  # Initialiserer figurer til visualiseringen
    first_index = 0 # Første index brukt


    #-----Leser inn verdier fra inputfil-----
    npunkt, punkt, nelem, elem, nlast, last, tverrsnitt = lesinput.lesinput('Inputfil-endelig.csv')

    punkt = np.array(punkt)
    elem = np.array(elem)
    tverrsnitt = np.array(tverrsnitt)


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
 
    # -----Fastinnspenningsreaksjoner og initialisering av lastvektor------
    fim = FastInnMom.FastInnMom(lastOb, elementOb, npunkt, nelem)
 
    R = fim.fib # Lastvektor

 
    # ------Setter opp systemstivhetsmatrisen-----
    K = SysStiMat.SysStiMat(elementOb, npunkt)

 
    # ------Innfører randbetingelser------
    K.randBet(punktOb, npunkt)

 
    # -----Løser ligningssystemet------
    rot = np.linalg.solve(K.K, R)

     
    #------Finner endemoment for hvert element-----
    endemoment = EndeMom.EndeMom(elementOb, rot).endeMom

 
    #-----Skriver ut hva rotasjonen ble i de forskjellige nodene-----
    print("Rotasjoner i de ulike punktene:")
    print(rot)
 
    #-----Skriver ut hva momentene ble for de forskjellige elementene-----
    print("Elementvis endemoment:")
    print(endemoment)

 
    #-----Plott ramme-----
    plot_structure(ax_init, punkt, elem, 1, first_index) # Plotter initialramme

    scaleRot = 10 # Skalerinng av rotasjoner
    scaleTrans = 10 # Skalering av translasjoner

    plot_structure_def(ax_def, punkt, elem, 1, first_index, rot, scaleRot, scaleTrans) # Plotter deformasjoner

  
    #-----Lager og plotter diagrammer-----
    Diagrammer.Diagrammer(elementOb, endemoment, nelem)
    
    #-----Regner på kapasitet for hvert bjelkeelement-----
    kap = Kapasitet.Kapasitet(elementOb)

    #-----Skriver ut kapasitet for bjelkene-----
    for i, kp in enumerate(kap.kapasitet):
        print(f'Bjelke: {elementOb[i].elem_n}, Tverrsnitt: {elementOb[i].tSnitt.type}, Kapasitet: {kp}')

    plt.show() # Viser figurer

    for emom in endemoment:
        print(f'P1-N: {emom[0]}, P1-V: {emom[1]}, P1-M: {emom[2]}, P2-N: {emom[3]}, P2-V: {emom[4]}, P2-M: {emom[5]}')

    

main_test()