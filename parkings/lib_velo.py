# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 19:33:11 2024

@author: franc
"""
    
import requests
import json
import time
    
def velo_time(Te, duree, fichier):
    # Demander les paramètres à l'utilisateur : 
    #Te = int(input("Période d'échantillonnage (en secondes) ? : ")) 
    #duree = int(input("Durée de l'acquisition (en secondes) ? : "))
    #fichier = input("Nom du fichier de sortie : ? ")
    output_file = open(fichier, 'w')

    # Calcul du nombre d'itérations
    nb_iterations = duree // Te

    print('traitement en cours...')
    for i in range(nb_iterations): # boucle de x s sur y mn

        response=requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
        dataV = response.json()  
        
        print('period : ', i)
        for velo in dataV:
            nom = velo['address']['value']['streetAddress']
            places_libres = velo['availableBikeNumber']['value']
            time_register = velo['availableBikeNumber']['metadata']['timestamp']['value']      
            places_tot = velo['totalSlotNumber']['value']  
            # On calcule le % de places dispo :
            taux_dispo = round(places_libres / places_tot *100,2)
        
            print(i, nom, places_tot, places_libres, taux_dispo, time_register)

            output_file.write(f"{str(i)}, {nom}, {str(places_tot)}, {str(places_libres)}, {str(taux_dispo)}, {time_register}\n")
     # mise en pause 10 secondes :          
        time.sleep(Te)

    output_file.close()


    
def list_velo():

    response=requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
    data_velo = response.json()
    with open('liste_velo.json', 'w') as file: json.dump(data_velo, file, indent=4)      
    
    ## récoupération d'une base velo pour l'ID (id de la liste pkg est <>)
    response=requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
    data = response.json()  # Convert the response to JSON data    
    with open('ID_velo.json', 'w') as file: json.dump(data, file, indent=4)  
    
    
    return data_velo

def charge_ID_velo(fic):
    with open(fic) as file: ID_velo = json.load(file)
    
    # sauvegarde pkg coordonnées en txt :
    fic2=fic.replace('JSON', 'TXT')
    output_file = open('localisation_station.txt', 'w')
    
    for station in ID_velo:
        ID = station['id']
        nom = station['address']['value']['streetAddress']
        places_tot = station['totalSlotNumber']['value']
        Coord = station['location']['value']['coordinates']
        output_file.write(f"{ID}, {nom}, {str(places_tot)}, {Coord[1]}, {Coord[0]}\n")    


    output_file.close()
        
    return ID_velo
    


def ID_velo(nom):

    with open('liste_velo.json') as file: list_velo = json.load(file)
   
    for velo in list_velo:
    
        # On reherche la station passé en param
        idV = velo['id']
        nomV = velo['address']['value']['streetAddress']
        if nom == nomV:
            return idV
    
    return('pkg non trouvé')

def histo_velo(id, nom, from_date, to_date):
    
    #velo_id = id #"urn:ngsi-ld :station :002 "
    velo_id = 'urn ngsi-ld station 001'
    #from_date = "2023-01-01" 
    #to_date = "2023-12-31" 
    #/bikestation_timeseries/{bikeStationId}/attrs/avai1ab1eBikeNumber    
    url = "https://portail-api-data.montpellier3m.fr/bikestation_timeseries/"+velo_id+"/attrs/avai1ab1eBikeNumber"

    params = {
      "fromDate": from_date,
      "toDate": to_date
    }

    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    fic= 'histoVelo_'+nom+'.json'
    with open(fic, 'w') as file: json.dump(data, file, indent=4)
    
    return data

def histo_velo2(id, nom, from_date, to_date):
    #response=requests.get("https://portail-api-data.montpellier3m.fr/bikestation_timeseries/urn%3Angsi-ld%3Astation%3A001/attrs/availableBikeNumber?fromDate=2022-12-31T00%3A00%3A00&toDate=2023-12-31T23%3A59%3A59")
   
    
    velo_id= 'urn%3Angsi-ld%3Astation%3A005' 
    velo_id2= id.replace(':','%3A')
    print(velo_id, velo_id2)
    url = "https://portail-api-data.montpellier3m.fr/bikestation_timeseries/urn%3Angsi-ld%3Astation%3A001/attrs/availableBikeNumber?fromDate=2022-12-31T00%3A00%3A00&toDate=2023-12-31T23%3A59%3A59"

    url1 = "https://portail-api-data.montpellier3m.fr/bikestation_timeseries/" + velo_id2 
    #url2 = "/attrs/availableBikeNumber?fromDate="+2023-01-01+"T00%3A00%3A00&toDate="+2023-12-31+"T23%3A59%3A59"
    url2 = "/attrs/availableBikeNumber?fromDate="+from_date+"T00%3A00%3A00&toDate="+to_date+"T23%3A59%3A59"
    url3 = url1+url2
    #print(url==url3)
    print(from_date, to_date)
    response=requests.get(url3)
    data = response.json()
    #print(data)
    fic= 'histoVelo_'+nom+'.json'
    with open(fic, 'w') as file: json.dump(data, file, indent=4)
    
    return data


    

def histo_velo_global(from_date, to_date):
    fichier = 'histoVelo_Global.json'
    dataG={}
    output_file = open(fichier, 'w')
    with open('ID_velo.json') as file: data2 = json.load(file)
    
    for velo in data2:
    
        idV = velo['id'] #"urn:ngsi-ld:parking:001"
        nomV = velo['address']['value']['streetAddress']
        print(idV, nomV)
        #from_date = "2023-01-01" 
        #to_date = "2023-12-31" 
        
        
        #/bikestation_timeseries/{bikeStationId}/attrs/avai1ab1eBikeNumber    
        url = "https://portail-api-data.montpellier3m.fr/bikestation_timeseries/"+idV+"/attrs/avai1ab1eBikeNumber"
           
        params = {
          "fromDate": from_date,
          "toDate": to_date
        }
    
        response = requests.get(url, params=params)
        data = response.json()
        #print(data)
        dataG.update(data) # cumul des data dans dataG
    
    json.dump(dataG, output_file, indent=4)
    output_file.close()
    return dataG    
    

def histo_veloT(from_date, to_date):

    with open('ID_velo.json') as file: data2 = json.load(file)
    
    for velo in data2:
    
        # On reherche la station passé en param
        idV = velo['id']
        nomV = velo['address']['value']['streetAddress']
        print(idV, nomV)
        
        #/bikestation_timeseries/{bikeStationId}/attrs/avai1ab1eBikeNumber    
        url = "https://portail-api-data.montpellier3m.fr/bikestation_timeseries/"+idV+"/attrs/avai1ab1eBikeNumber"
        
        params = {
           "fromDate": from_date,
           "toDate": to_date
        }    
        response = requests.get(url, params=params)
        data = response.json()
        print(data)
        fic= 'histoVelo_'+nomV+'.json'
        with open(fic, 'w') as file: json.dump(data, file, indent=4)



def histo_veloT2(from_date, to_date):

    with open('ID_velo.json') as file: data2 = json.load(file)
    
    for velo in data2:
    
        # On reherche la station passé en param
        idV = velo['id']
        velo_id2= idV.replace(':','%3A')
        nomV = velo['address']['value']['streetAddress']
        print(idV, nomV)
        
        #/bikestation_timeseries/{bikeStationId}/attrs/avai1ab1eBikeNumber    
        url = "https://portail-api-data.montpellier3m.fr/bikestation_timeseries/"+idV+"/attrs/avai1ab1eBikeNumber"
        url1 = "https://portail-api-data.montpellier3m.fr/bikestation_timeseries/" + velo_id2 
        url2 = "/attrs/availableBikeNumber?fromDate="+from_date+"T00%3A00%3A00&toDate="+to_date+"T23%3A59%3A59"
        url3 = url1+url2
            
        response = requests.get(url3)
        data = response.json()
        print(data)
        fic= 'histoVelo_'+nomV+'.json'
        with open(fic, 'w') as file: json.dump(data, file, indent=4)
        

def velo_fic_histo(nomV):
    fic= 'histoVelo_'+nomV+'.json'
    with open(fic) as file: data2 = json.load(file)
    print('import '+fic)
    return(data2)
    

def get_jour(mois):
    # renvoie le nombre de jours en fonction du mois
    if mois == 1 or mois == 3 or mois == 5 or mois == 7 or mois == 8 or mois == 10 or mois == 12:
        jj = 31
    if mois == 4 or mois == 6 or mois == 9 or mois == 11:
        jj = 30
    if mois == 2:
        jj = 27
    return jj


def merged_data2(data_cumul, data):
  
    # Ajoutez les nouvelles valeurs des listes.
    data_cumul["index"].extend(data["index"])
    data_cumul["values"].extend(data["values"])
      
    return data_cumul


    
def trait_compl_velo():

# boucle sur les parkings : 

    # ID_pkg2.json (source sans 2 pkgs Gaumont vides) 
    with open('json/ID_velo.json') as file: list_velo = json.load(file)
   
    for park in list_velo:
        # init : 
        dataG={}
        bcl = 0 
        idV = park['id']
        nomV = park['address']['value']['streetAddress']
        print(idV, nomV)
         
        # boucle sur les periodes :            
        for mois in range(1, 12+1):
            bcl = bcl + 1
            if mois < 10:
                Cmois =  '0'+ str(mois)
            else:
                Cmois =  str(mois)
            #from_date = "2023-01-01" 
            #to_date = "2023-12-31" 
                    
            from_date = "2023-"+ Cmois + "-01" 
            jj = '-'+str(get_jour(mois))
            to_date = "2023-"+ Cmois + jj
            print(from_date, to_date)
            # récupérer data :         
            #data = histo_pkg(idP, nomP, from_date, to_date)   
            
            url1 = "https://portail-api-data.montpellier3m.fr/bikestation_timeseries/" + idV 
            #url2 = "/attrs/availableBikeNumber?fromDate="+2023-01-01+"T00%3A00%3A00&toDate="+2023-12-31+"T23%3A59%3A59"
            url2 = "/attrs/availableBikeNumber?fromDate="+from_date+"T00%3A00%3A00&toDate="+to_date+"T23%3A59%3A59"
            url3 = url1+url2            
            response=requests.get(url3)
            data = response.json()                      
            print(len(data))
            if len(data) < 5:
                bcl= bcl-1
            else:
                if bcl == 1:
                    dataG = data
                else:
                    # cumul avec autres data :
                    dataG = merged_data2(dataG, data)
                #print(dataG)
            print('mois :', mois)
            
        
        # sauvegarde json sur disque :     
        fic= 'json/histoVelo_'+nomV+'.json'
        with open(fic, 'w') as file: json.dump(dataG, file, indent=4)
        #ss = input('stop')    

def trait_compl_velo2():

# boucle sur les parkings : 

    # ID_pkg2.json (source sans 2 pkgs Gaumont vides) 
    with open('json/ID_velo.json') as file: list_velo = json.load(file)
   
    for park in list_velo:
        # init : 
        dataG={}
        bcl = 0 
        idV = park['id']
        nomV = park['address']['value']['streetAddress']
        print(idV, nomV)
         
        # boucle sur les periodes :            
        for mois in range(1, 12+1):
            
            if mois < 10:
                Cmois =  '0'+ str(mois)
            else:
                Cmois =  str(mois)
            #from_date = "2023-01-01" 
            #to_date = "2023-12-31" 
            
            for jour in range(1,31):
                bcl = bcl + 1
                if jour<10:
                    jj='0'+str(jour)
                else:
                    jj=str(jour)
                from_date = "2023-"+ Cmois + "-"+jj 
                to_date = "2023-"+ Cmois + "-"+jj
                print(from_date, to_date)
                # récupérer data :         
                #data = histo_pkg(idP, nomP, from_date, to_date)   
                #fromDate=2023-02-01T00%3A00%3A00&toDate=2023-02-01T24%3A00%3A00
                url1 = "https://portail-api-data.montpellier3m.fr/bikestation_timeseries/" + idV 
                #url2 = "/attrs/availableBikeNumber?fromDate="+2023-01-01+"T00%3A00%3A00&toDate="+2023-12-31+"T23%3A59%3A59"
                url2 = "/attrs/availableBikeNumber?fromDate="+from_date+"T00%3A00%3A00&toDate="+to_date+"T23%3A59%3A59"
                url3 = url1+url2            
                response=requests.get(url3)
                data = response.json()
                #print(data)                          
                #print('len data', len(data), bcl)
                
                if len(data) < 5 or len(data)> 100:
                    bcl= bcl-1
                else:
                    if bcl == 1:
                        dataG = data
                    else:
                        # cumul avec autres data :
                        dataG = merged_data2(dataG, data)
                    #print(dataG)
            print('mois :', mois)
            
        
        # sauvegarde json sur disque :     
        fic= 'json/histoVelo_'+nomV+'.json'
        with open(fic, 'w') as file: json.dump(dataG, file, indent=4)
        #ss = input('stop')       
    
def verif_velo():

# boucle sur les parks velo : 

    # ID_pkg2.json (source sans 2 pkgs Gaumont vides) 
    with open('json/ID_velo.json') as file: list_velo = json.load(file)
   
    for park in list_velo:
        # init : 

        idV = park['id']
        nomV = park['address']['value']['streetAddress']
        List=[]
        fic= 'json/histoVelo_'+nomV+'.json'
        
        with open(fic) as park_file:
          park_data = json.load(park_file)
          timestamps = park_data['index']
          values = park_data['values']
          min_date ="99-99-99" 
          max_date ="00-00-00" 
          cpt_jour = 0
          anc_jour =''
          for ts, val in zip(timestamps, values):
              #'2023-01-04'
              jour = ts[:10]
              #print(jour)
              
              if jour != anc_jour:
                  List.append(jour)
                  cpt_jour = cpt_jour+1
                  anc_jour =jour
                  
                  
              if ts > max_date:
                  max_date = ts
              if ts < min_date:
                  min_date = ts
          print(idV, nomV, 'nb jours base :', cpt_jour)    
          print('min-max date :', min_date, max_date)
          #print(List)
          #ss=input('stop')            