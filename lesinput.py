import csv
import numpy as np


#Inputfilen tar inn CSV-filer, der hver verdi er separert med ";". 
#Returnerer lister på samme form som den utdelte koden er bygget opp for
def lesinput(fil):
    # Åpner inputfilen
    with open(fil) as fil:
        csv_reader = csv.reader(fil, delimiter = ';') 
        #Definerer de ulike arrayene som skal fylles med data
        nodearray = [] 
        beamarray = []
        lastarray = []
        geoarray = []
        geoCount = 0 #initialiserer starten av geometri-arrayen
        
        
        
        for row in csv_reader: #

           
            if (row[0])[-5:]=='Nodes': #Definerer antall punkter og laster, angitt på samme linje som ordet "Nodes" i excel-fila
                npunkt= int(row[1])
                nlast = int(row[3])
                
                
            elif (row[0])[-5:]=='Beams': #Leser av antall bjelkeelementer, angitt etter ordet "Beams" i excel-fila
                nelem = int(row[1])
                

            elif (row[0]=='Node'): #Leser av alle linjer med der ordet "Node" står i første celle
                idTemp = int(row[1])
                xTemp = float(row[2])
                yTemp = float(row[3])
                fxTemp = float(row[4])
                fyTemp = float(row[5])
                mTemp = float(row[6])
                tempMatrise = np.array([xTemp, yTemp, (fxTemp,fyTemp,mTemp)], dtype=object) 
                nodearray.append(tempMatrise) #Fyller knutepunktslista med knutepunktverdiene fra excel-arket
                

            elif (row[0]=='Beam'): #Leser av alle linjer med der ordet "Beam" står i første celle
                idTemp = int(row[1])
                node1Temp = int(row[2])
                node2Temp = int(row[3])
                geoTemp = int(row[4])
                flytspenning = float(row[5])
                beamArrayTemp = np.array([idTemp,node1Temp,node2Temp,geoTemp,flytspenning])
                beamarray.append(beamArrayTemp) #Fyller bjelke-lista med bjelkeverdiene fra excel-arket
                
              
           
            elif ((row[0])[:3]=='Pun' or (row[0])[:3]=='For'): #Leser av alle linjer med der første celle er "Punktlast..." eller "Fordelt last..."
                typeTemp = int(row[1]) 
                vinkelTemp = float(row[6])
                intensTemp = float(row[7])
                x1Temp = float(row[2])
                y1Temp = float(row[3])
                x2Temp = float(row[4])
                y2Temp = float(row[5])
                lastArrayTemp = np.array([typeTemp, x1Temp, y1Temp, x2Temp, y2Temp, vinkelTemp, intensTemp])
                lastarray.append(lastArrayTemp)  #Fyller last-lista med lastverdier fra excel-arket
                
                

            elif ((row[0])[:3]=='Geo'): #indikerer at man er i nederste tabell, der geometri-informasjon finnes
                geoCount = 1
                

            elif (geoCount ==1 and row[0]!= ''): #kjører ut nederste tabell
                geoTemp = int(row[1])
                BTemp = float(row[2])
                bTemp = float(row[3])
                HTemp = float(row[4])
                hTemp = float(row[5])
                Rtemp = float(row[6])
                rTemp = float(row[7])
                t_stegTemp = float(row[8])
                t_flensTemp = float(row[9])
                mat_typeTemp = int(row[10])
                ETemp = float(row[11])
                geoArrayTemp = np.array([geoTemp, BTemp,bTemp,HTemp,hTemp,Rtemp,rTemp,t_stegTemp,t_flensTemp ,mat_typeTemp ,ETemp])
                geoarray.append(geoArrayTemp) #Fyller geometri-lista med geometriverdier fra excelarket 
                


            else :
                continue 
    
    
    #Returnerer antall knutepunkter, knutepunktslista, antall bjelkeelementer, bjelkelista, antall laster, lastlista og geometrilista
    return npunkt,nodearray, nelem, beamarray, nlast, lastarray, geoarray 