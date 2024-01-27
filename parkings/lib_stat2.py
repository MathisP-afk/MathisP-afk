# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:55:08 2024

@author: FlowUp
"""
import json
import datetime
import re

def comptage_depassement(data, seuil):

  nombres = {'heures': {}, 'jours':{}}

  timestamps = data['index']
  values = data['values']  

  for timestamp, value in zip(timestamps, values):

    dt = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')

    if value > seuil:

      key_heure = dt.hour
      key_jour = dt.date()  

      if key_heure not in nombres['heures']:
        nombres['heures'][key_heure] = 0

      if key_jour not in nombres['jours']:    
        nombres['jours'][key_jour] = 0

      nombres['heures'][key_heure] += 1  
      nombres['jours'][key_jour] += 1
      
    #print(key_heure)
    #convert_HJ = round(nombres['heures'].values()/24,1)
  print(f"Nombre d'heures au-dessus du seuil ({seuil}): {sum(nombres['heures'].values())}, équivalents jours : {round(sum(nombres['heures'].values())/24,1)}")
  print(f"Nombre de jours au-dessus du seuil ({seuil}): {len(nombres['jours'])}")

def test_timestamp(ts):
    #timestamp_regex = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{2}:\d{2}'
    #timestamp_regex = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}'
    timestamp_regex = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{2}:\d{2}'
            
    
    if not re.match(timestamp_regex, ts):
        print(f"Timestamp incorrect: {ts}")
        return False
    return True


def get_capacity(ID):
    
    with open('ID_pkg.json') as file: list_pkg = json.load(file)
   
    for parking in list_pkg:
    
        # On reherche le parking passé en param
        idP = parking['id']
        nomP = parking['name']['value']
        capacite = parking['totalSpotNumber']['value']
        #print(ID, idP, capacite)
        if ID == idP:
            return capacite 

def imp_fic_histo(nomP):
    fic= 'histo_'+nomP+'.json'
    with open(fic) as file: data2 = json.load(file)
    print('import '+fic)
    return(data2)        


def comptage_depassement_pkgT(taux):
    with open('ID_pkg2.json') as file: data2 = json.load(file)
    for parking in data2:
        id_P = parking['id'] #"urn:ngsi-ld:parking:001"
        nom_P = parking['name']['value']
        print(id_P, nom_P)
        capacity = get_capacity(id_P)

        seuil = capacity * taux
        print("capacity", capacity)

        # récupération de la base historique d'un pkg préalablement enregistré sur disque :
        #nom_P= 'Corum'
        data_E = imp_fic_histo(nom_P)
        comptage_depassement(data_E, seuil)  


def test_base(fic):
    with open(fic) as file: data = json.load(file)
    timestamps = data['index']
    values = data['values']  
    for timestamp, value in zip(timestamps, values):
        dt = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
        key_heure = dt.hour
        if key_heure <0 or key_heure >24:
            print('erreur Heure', key_heure)
        else:
            print(key_heure)            
            
        if not test_timestamp(str(dt)):
            continue
        #print(timestamp, dt)   

        