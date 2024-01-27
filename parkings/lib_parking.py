# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 19:33:11 2024

@author: franc
"""
import requests
import json
import time

    
def parking_time(Te, duree, fichier):
    # Demander les paramètres à l'utilisateur : 
    #Te = int(input("Période d'échantillonnage (en secondes) ? : ")) 
    #duree = int(input("Durée de l'acquisition (en secondes) ? : "))
    #fichier = input("Nom du fichier de sortie : ? ")
    output_file = open(fichier, 'w')

    # Calcul du nombre d'itérations
    nb_iterations = duree // Te

    print('traitement en cours...')
    for i in range(nb_iterations): # boucle de x s sur y mn

        response = requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
        data = response.json()  
        
        print('period : ', i)
        for parking in data:
            nom = parking['name']['value']
            places_libres = parking['availableSpotNumber']['value']
            time_register = parking['availableSpotNumber']['metadata']['timestamp']['value']      
            places_tot = parking['totalSpotNumber']['value']  
            # On calcule le % de places dispo :
            taux_dispo = round(places_libres / places_tot *100,2)
        
            print(i, nom, places_tot, places_libres, taux_dispo, time_register)

            output_file.write(f"{str(i)}, {nom}, {str(places_tot)}, {str(places_libres)}, {str(taux_dispo)}, {time_register}\n")
     # mise en pause 10 secondes :          
        time.sleep(Te)

    output_file.close()
    
    


def list_pkg():
    response=requests.get("https://portail-api-data.montpellier3m.fr/parkingspaces?limit=1000")
    data_pkg = response.json()
    with open('liste_pkg.json', 'w') as file: json.dump(data_pkg, file, indent=4)      

    ## récupération d'une base pkg pour l'ID (id de la liste pkg est <>)
    response=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    data = response.json()  # Convert the response to JSON data    
    with open('ID_pkg.json', 'w') as file: json.dump(data, file, indent=4)  
    
    return data_pkg

def charge_ID_pkg(fic):
    with open(fic) as file: ID_pkg = json.load(file)
    
    # sauvegarde pkg coordonnées en txt :
    fic2=fic.replace('JSON', 'TXT')
    output_file = open('localisation_pkg.txt', 'w')
    
    for parking in ID_pkg:
        ID = parking['id']
        nom = parking['name']['value']
        places_tot = parking['totalSpotNumber']['value']
        Coord = parking['location']['value']['coordinates']
        output_file.write(f"{ID}, {nom}, {str(places_tot)}, {Coord[1]}, {Coord[0]}\n")    


    output_file.close()
        
    return ID_pkg

    

def ID_pkg(nom):
    with open('ID_pkg.json') as file: list_pkg = json.load(file)
   
    for parking in list_pkg:
    
        # On reherche le parking passé en param
        idP = parking['id']
        nomP = parking['name']['value']
        if nom == nomP:
            return idP
    
    return('pkg non trouvé')

def ID_velo(nom):
    with open('liste_velo.json') as file: list_velo = json.load(file)
   
    for velo in list_velo:
    
        # On reherche le parking passé en param
        idV = velo['id']
        nomV = velo['address']['value']['streetAddress']
        if nom == nomV:
            return idV
    
    return('pkg non trouvé')

def histo_pkg(id, nom, from_date, to_date):
   
    parking_id = id #"urn:ngsi-ld:parking:001"
    #from_date = "2023-01-01" 
    #to_date = "2023-12-31" 
    
    url = "https://portail-api-data.montpellier3m.fr/parking_timeseries/"+parking_id+"/attrs/availableSpotNumber"

    params = {
      "fromDate": from_date,
      "toDate": to_date
    }

    response = requests.get(url, params=params)
    data = response.json()
    #print(data)
    #fic= 'histo_'+nom+'.json'
    #with open(fic, 'w') as file: json.dump(data, file, indent=4)
    
    return data
    

def histo_pkg_global(from_date, to_date):
    fichier = 'histo_Global.json'
    dataG={}
    output_file = open(fichier, 'w')
    with open('ID_pkg.json') as file: data2 = json.load(file)
    
    for parking in data2:
    
        parking_id = parking['id'] #"urn:ngsi-ld:parking:001"
        nomP = parking['name']['value']
        print(parking_id, nomP)
        #from_date = "2023-01-01" 
        #to_date = "2023-12-31" 
        
        url = "https://portail-api-data.montpellier3m.fr/parking_timeseries/"+parking_id+"/attrs/availableSpotNumber"
    
        params = {
          "fromDate": from_date,
          "toDate": to_date
        }
    
        response = requests.get(url, params=params)
        data = response.json()
        #print(data)
        dataG.update(data)
    
    json.dump(dataG, output_file, indent=4)
    output_file.close()
    return dataG    
    

def histo_pkgT(from_date, to_date):

    with open('ID_pkg.json') as file: data2 = json.load(file)
    
    for parking in data2:
    
        parking_id = parking['id'] #"urn:ngsi-ld:parking:001"
        nomP = parking['name']['value']
        print(parking_id, nomP)
        
        
        #parking_id = id #"urn:ngsi-ld:parking:001"
        #from_date = "2023-01-01" 
        #to_date = "2023-12-31" 
        
        url = "https://portail-api-data.montpellier3m.fr/parking_timeseries/"+parking_id+"/attrs/availableSpotNumber"
    
        params = {
          "fromDate": from_date,
          "toDate": to_date
        }
    
        response = requests.get(url, params=params)
        data = response.json()
        print(data)
        fic= 'histo_'+nomP+'.json'
        with open(fic, 'w') as file: json.dump(data, file, indent=4)
    

def imp_fic_histo(nomP):
    fic= 'json/histo_'+nomP+'.json'
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

def merged_data(data_cumul, data):
    # Copier les champs simples  
    data_cumul['attrName'] = data['attrName']
    data_cumul['entityId'] = data['entityId'] 
    data_cumul['entityType'] = data['entityType']
    
    # test index :
    if 'index' not in data_cumul:
        data_cumul['index'] = []
  
    # Concaténer les listes
    data_cumul['index'] += data['index']
    data_cumul['values'] += data['values']

    return data_cumul

def merged_data2(data_cumul, data):
  
    # Ajoutez les nouvelles valeurs des listes.
    data_cumul["index"].extend(data["index"])
    data_cumul["values"].extend(data["values"])
      
    return data_cumul


def trait_pkg(idP, nomP):

    # init : 
    dataG={}
    bcl = 0 
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
        jj = '-'+ str(get_jour(mois))
        to_date = "2023-"+ Cmois + jj
        print(bcl, from_date, to_date)
        
        # récupérer data :         
        data = histo_pkg(idP, nomP, from_date, to_date)   
        #print(data)
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
        
    print(dataG)
    # sauvegarde json sur disque :     
    fic= 'json/histo_'+nomP+'.json'
    with open(fic, 'w') as file: json.dump(dataG, file, indent=4)
    #ss = input('stop')
    


def trait_compl_pkg():

# boucle sur les parkings : 

    # ID_pkg2.json (source sans 2 pkgs Gaumont vides) 
    with open('json/ID_pkg2.json') as file: list_pkg = json.load(file)
   
    for parking in list_pkg:
        # init : 
        dataG={}
        bcl = 0 
        idP = parking['id']
        nomP = parking['name']['value']
        print(idP, nomP)
         
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
            data = histo_pkg(idP, nomP, from_date, to_date)   
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
        fic= 'json/histo_'+nomP+'.json'
        with open(fic, 'w') as file: json.dump(dataG, file, indent=4)
        #ss = input('stop')




def verif_pkg():

# boucle sur les parkings : 

    # ID_pkg2.json (source sans 2 pkgs Gaumont vides) 
    with open('json/ID_pkg2.json') as file: list_pkg = json.load(file)
   
    for parking in list_pkg:
        # init : 

        idP = parking['id']
        nomP = parking['name']['value']
        List=[]
        fic= 'json/histo_'+nomP+'.json'
        
        with open(fic) as parking_file:
          parking_data = json.load(parking_file)
          timestamps = parking_data['index']
          values = parking_data['values']
          min_date ="99-99-99" 
          max_date ="00-00-00" 
          cpt_jour = 0
          anc_jour =''
          for ts, val in zip(timestamps, values):
              #'2023-01-04'
              jour = ts[:10]
              #print(jour)
              
              if jour != anc_jour:
                  #List.append(jour)
                  cpt_jour = cpt_jour+1
                  anc_jour =jour
                  
                  
              if ts > max_date:
                  max_date = ts
              if ts < min_date:
                  min_date = ts
          print(idP, nomP, 'nb jours base :', cpt_jour)    
          print('min-max date :', min_date, max_date)
          #print(List)
          #ss=input('stop')        