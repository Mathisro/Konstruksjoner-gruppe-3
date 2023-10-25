import csv

def lesinput(fil):
    # Åpner inputfilen
    with open(fil) as fil:
        csv_reader = csv.reader(fil, delimiter = ',')
        nodearray = [] #Definerer de ulike arrayene
        beamarray = []
        lastarray = []
        geoarray = []
        geoCount = 0
        #print("Header utført")
        
        
        for row in csv_reader:

           
            if (row[0])[-5:]=='Nodes': #Leser av første linje
                npunkt= float(row[1])
                nlast = float(row[3])
                print("First row reading")
                
            elif (row[0])[-5:]=='Beams': #Leser av andre linje
                nelem = float(row[1])
                ntverr = (row[3])
                #print("second row reading")

            elif (row[0]=='Node'): #Leser av alle linjer med "Node"
                idTemp = (row[1])
                xTemp = (row[2])
                yTemp = (row[3])
                fxTemp = (row[4])
                fyTemp = (row[5])
                mTemp = (row[6])
                tempMatrise = [idTemp,xTemp, yTemp, fxTemp,fyTemp,mTemp]
                nodearray.append(tempMatrise)
                #print("Node reading")

            elif (row[0]=='Beam'): #Leser av alle linjer med "Beam"
                idTemp = (row[1])
                node1Temp = (row[2])
                node2Temp =(row[3])
                geoTemp = (row[4])
                ukjent = (row[5])
                beamArrayTemp = [idTemp,node1Temp,node2Temp,geoTemp,ukjent]
                beamarray.append(beamArrayTemp)
                #print("Beam reading")
              
            #type: 1 hvis punktlast, 2 hvis fordelt last 
            #intensitet
            #startpunkt
            #sluttpunkt, (null hvis punktlast)
            #retning (vinkel)
            #type fordelt last (1-7)
            elif ((row[0])[:3]=='Pun' or (row[0])[:3]=='For'): #Leser av alle linjer med "Punktlast..." eller "Fordelt last..."
                idTemp = row[1]
                nodeIdTemp = row[2]
                typeTemp = row[3]
                vinkelTemp = row[4]
                intensTemp = row[5]
                startPunktTemp = row[6]
                sluttPunktTemp = row[7]
                lastArrayTemp = [typeTemp,intensTemp,startPunktTemp, sluttPunktTemp,vinkelTemp,idTemp,nodeIdTemp]
                lastarray.append(lastArrayTemp)
                #print("Last reading")
                

            elif ((row[0])[:3]=='Geo'): #indikerer at man er i nederste tabell
                geoCount = 1
                #print("start nedre tabell")

            elif (geoCount ==1 and row[0]!= ''): #kjører ut nederste tabell
                geoTemp = row[0]
                BTemp = row[1]
                bTemp = row[2]
                HTemp = row[3]
                hTemp = row[4]
                Rtemp = row[5]
                rTemp = row[6]
                t_stegTemp = row[7]
                t_flensTemp = row[8]
                mat_typeTemp = row[9]
                ETemp = row[10]
                geoArrayTemp = [geoTemp, BTemp,bTemp,HTemp,hTemp,Rtemp,rTemp,t_stegTemp,t_flensTemp ,mat_typeTemp ,ETemp]
                geoarray.append(geoArrayTemp) 
                #print("geometry reading")


            else :
                continue 
    
    
    return npunkt,nodearray, nelem, beamarray, nlast, lastarray, ntverr, geoarray

values = lesinput("C:\MarineKonstruksjoner\inputfil25.1.csv")

#for i in range(8): 
    #print(values[i])

#print(values[])
