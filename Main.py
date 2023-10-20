from structureVisualization import *
import numpy as np
import Punkt
import Last
import Element
import lesinput
import FastInnMom
import SysStiMat
import Tverrsnitt
 
# -----Rammeanalyse-----
def main():
    
    # Plotter figurer
    # 
    
    fig_init, ax_init, fig_def, ax_def = setup_plots()  # Initialiserer figurer til visualiseringen
    first_index = 0 # Første index brukt

    npunkt, punkt, nelem, elem, nlast, last, tverrsnitt = lesinput.lesinput() # Leser input-data
 
    plot_structure(ax_init, punkt, elem, 1, first_index) # Plotter initalramme
 
    # Regner ut lengder til elementene
    # elementlengder = lengder(punkt, elem, nelem) ## Gjøres i hvert objekt

    # Initialiserer liste med alle objektene

    tverrsnittOb = []
    for i in range(len(tverrsnitt)):
        tverrsnittOb.append(Tverrsnitt.Tverrsnitt(tverrsnitt[i]))

    punktOb = np.zeros(npunkt)
    for i in range(npunkt):
        punktOb[i] = Punkt.Punkt(i, punkt[i])
        
    elementOb = np.zeros(nelem)
    for i in range(nelem):
        elementOb[i] = Element.Element(i, elem[i], tverrsnittOb)

    lastOb = np.zeros(nlast)
    for i in range(nlast):
        lastOb[i] = Last.Last(i, last[i])


 
    # -----Fastinnspenningsmomentene------
    # Lag funksjonen selv
    fim = FastInnMom.FastInnMom(lastOb, elementOb, npunkt, nelem)
 
    # -----Setter opp lastvektor-----
    # Lag funksjonen selv
    b = fim.fib
 
    # ------Setter opp systemstivhetsmatrisen-----
    # Lag funksjonen selv
    K = SysStiMat.SysStiMat(elementOb, nelem)
 
    # ------Innfører randbetingelser------
    # Lag funksjonen selv
    K.randBet(elementOb)
 
    # -----Løser ligningssystemet------
    # Lag funksjonen selv
    rot = np.linalg.solve(K.K, b)
    # Hint, se side for løsing av lineære systemer i Python
     
    #------Finner endemoment for hvert element-----
    # Lag funksjonen selv
    endemoment = endeM(npunkt, punkt, nelem, elem, elementlengder, rot, fim)
 
    #-----Skriver ut hva rotasjonen ble i de forskjellige nodene-----
    print("Rotasjoner i de ulike punktene:")
    print(rot)
 
    #-----Skriver ut hva momentene ble for de forskjellige elementene-----
    print("Elementvis endemoment:")
    print(endemoment)
 
    #-----Plott deformert ramme-----
    skalering = 100;     # Du kan endre denne konstanten for å skalere de synlige deformasjonene til rammen
    plot_structure_def(ax_def, punkt, elem, 1, first_index, skalering*rot)
    plt.show()