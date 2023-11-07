# ----Importer biblioteker og filer----
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

# -----Rammeanalyse-----
def main():
    
    #-----Klargjør for plotting med utdelt kode-----
    fig_init, ax_init, fig_def, ax_def = setup_plots()  # Initialiserer figurer til visualiseringen
    first_index = 0 # Første index brukt


    #-----Leser inn verdier fra inputfil-----
    npunkt, punkt, nelem, elem, nlast, last, tverrsnitt = lesinput.lesinput('Inputfil_portal.csv')

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

    

main()