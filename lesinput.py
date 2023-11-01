import csv
import numpy as np

def lesinput(fil):
    # Åpner inputfilen
    with open(fil) as fil:
        csv_reader = csv.reader(fil, delimiter = ';')
        nodearray = [] #Definerer de ulike arrayene
        beamarray = []
        lastarray = []
        geoarray = []
        geoCount = 0
        #print("Header utført")
        
        
        for row in csv_reader:

           
            if (row[0])[-5:]=='Nodes': #Leser av første linje
                npunkt= int(row[1])
                nlast = int(row[3])
                #print("First row reading")
                
            elif (row[0])[-5:]=='Beams': #Leser av andre linje
                nelem = int(row[1])
                #ntverr = int(row[3])
                #print("second row reading")

            elif (row[0]=='Node'): #Leser av alle linjer med "Node"
                idTemp = int(row[1])
                xTemp = float(row[2])
                yTemp = float(row[3])
                fxTemp = float(row[4])
                fyTemp = float(row[5])
                mTemp = float(row[6])
                tempMatrise = np.array([xTemp, yTemp, (fxTemp,fyTemp,mTemp)])
                nodearray.append(tempMatrise)
                #print("Node reading")

            elif (row[0]=='Beam'): #Leser av alle linjer med "Beam"
                idTemp = int(row[1])
                node1Temp = int(row[2])
                node2Temp = int(row[3])
                geoTemp = int(row[4])
                flytspenning = float(row[5])
                beamArrayTemp = np.array([idTemp,node1Temp,node2Temp,geoTemp,flytspenning])
                beamarray.append(beamArrayTemp)
                #print("Beam reading")
              
            #type: 1 hvis punktlast, 2 hvis fordelt last 
            #intensitet
            #startpunkt
            #sluttpunkt, (null hvis punktlast)
            #retning (vinkel)
            #type fordelt last (1-7)
            elif ((row[0])[:3]=='Pun' or (row[0])[:3]=='For'): #Leser av alle linjer med "Punktlast..." eller "Fordelt last..."
                #idTemp = int(row[1])
                #nodeIdTemp = int(row[2])
                typeTemp = int(row[1])
                vinkelTemp = float(row[6])
                intensTemp = float(row[7])
                x1Temp = float(row[2])
                y1Temp = float(row[3])
                x2Temp = float(row[4])
                y2Temp = float(row[5])
                lastArrayTemp = np.array([typeTemp, x1Temp, y1Temp, x2Temp, y2Temp, vinkelTemp, intensTemp])
                lastarray.append(lastArrayTemp)
                #print("Last reading")
                

            elif ((row[0])[:3]=='Geo'): #indikerer at man er i nederste tabell
                geoCount = 1
                #print("start nedre tabell")

            elif (geoCount ==1 and row[0]!= ''): #kjører ut nederste tabell
                geoTemp = int(row[0])
                BTemp = float(row[1])
                bTemp = float(row[2])
                HTemp = float(row[3])
                hTemp = float(row[4])
                Rtemp = float(row[5])
                rTemp = float(row[6])
                t_stegTemp = float(row[7])
                t_flensTemp = float(row[8])
                mat_typeTemp = int(row[9])
                ETemp = float(row[10])
                geoArrayTemp = np.array([geoTemp, BTemp,bTemp,HTemp,hTemp,Rtemp,rTemp,t_stegTemp,t_flensTemp ,mat_typeTemp ,ETemp])
                geoarray.append(geoArrayTemp) 
                #print("geometry reading")


            else :
                continue 
    
    
    return npunkt,nodearray, nelem, beamarray, nlast, lastarray, geoarray


#for i in range(8): 
    #print(values[i])

#print(values[])
