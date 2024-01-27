# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 10:42:21 2024

@author: Mathis
"""
# In[0] :repertoire de travail :
import os
dir_pkg = "D:\Documents\Mathis\IUT\Année_1\informatique\Parking_json"
os.chdir(dir_pkg)

# In[1] :requete
import requests
response=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000") 
print(response.text)

""" Exécuter le code python suivant et expliquer ce qu’il fait :

Ce code envoie une requête au serveur contenant les données sur les parkings de Montpellier
grâce à la librairie : 'requests' et la méthode 'get'
et récupère le résultat de la requête dans la variable 'response'
puis le résultat est affiché par la fonction 'print'
extrait :
{"type":"Point","coordinates":[3.88881893,43.60871606]},"metadata":{}},
"name":{"type":"Text","value":"Antigone","metadata":{}},"requiredPermit":{"type":"Text",
"value":"noPermitNeeded","metadata":{}},"status":{"type":"Text","value":"Open",
"metadata":{"timestamp"
     
"""


# In[2] : JSON
import requests
import json
response=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
data = response.json()  # Convert the response to JSON data


""" Sous quel format est converti la réponse ? :
Si les donnéees récupérées dans la variable 'response', sont formatées en json, 
elles sont stockées dans une seule variable, peu exploitable en Python.
Pour pouvoir être traitées, elles doivent être transférée dans un tableau de données 
sous forme de liste par la méthode 'response.json()' 
la variable 'data' est une liste qui contient des dictionnaires (clef:valeur)

Qu’en est-il de son contenu ? 
Son contenu est maintenant présenté sous forme de tableau 
pour lequel chaque ligne correspond à un parking, 
chaque colonne à une inforrmation concernant le parking : 
    - son identifiant
    - son nom
    - ses coordonnées géographiques (lat., long.)
    - sa disponibilité,...

Décrivez comment un fichier json est construit :
 JSON est un format qui permet de stocker des informations structurées
- Les données sont présentées sous forme de paires clé/valeur.
- ':' est placé entre chaque clé et chaque valeur
- Les éléments de données sont séparés par des virgules.
- Les crochets {} désignent les objets.
- Les crochets [] désignent des tableaux.
{“key”:“value”,“key”:“value”,“key”:“value”.}

le fichier json récupéré est une liste de dicntionnaire contenant :
    - le type de la donnée (Text, Number)
    - la valeur (value)
    - la metadata (dictionnaire décrivant la donnée)
"""

# In[3] : ecriture JSON
with open('data.json', 'w') as file: json.dump(data, file, indent=4)

""" Que fait ce code ?
suvegarde de la list 'data', dans un fichier dénommé 'data.json' :
    - open('data.json', 'w') ouvre le fichier data.json en mode écriture ('w')
    - as file associe le fichier ouvert à la variable file
    - json.dump prend en entrée les données à écrire sous forme JSON (data) 
    - indent=4 indique que le JSON doit être indenté avec 4 espaces
"""

# In[4] : lecture JSON
with open('data.json') as file: data2 = json.load(file)
print(data2)

""" Que fait ce code ?
ouverture du fichier précédemment enregistré pour lecture : 
 - open('data.json') ouvre le fichier data.json en mode lecture seule
 - as file associe le fichier ouvert à la variable file
 - json.load prend en entrée le fichier ouvert contenant le JSON 
 - Il retourne les données chargées sous forme d'objet Python
 - Ces données sont attribuées à la variable data2 (liste de dictionnaires),
 identique à la liste initiale
""" 
 # In[5] : PLACES LIBRES 
"""
Ecrire un programme qui récupère le nombre de places libres dans chaque parking 
et qui sauvegarde ces données dans un fichier texte (une donnée par ligne 
contenant uniquement le nombre de places libres. 
Il faudra vérifier pour chaque parking, s’il est ouvert.

- modifier votre programme pour sauvegarder un fichier contenant dans 
chaque ligne : le nom du parking puis le nombre de places libres.

"""
import json
# Ouverture du fichier json contenant les données sur les parkings
with open('data.json') as parking_file:
  parking_data = json.load(parking_file)

# Ouverture du fichier texte où seront écrites les places libres
places_libres_file = open('places_libres.txt', 'w')

for parking in parking_data:

    # On vérifie que le parking est ouvert
    statut = parking['status']['value']
    nom = parking['name']['value']
    
    if statut == 'Open':
        # On récupère le nombre de places disponibles
        places_libres = parking['availableSpotNumber']['value']
        # Ecriture de la donnée dans le fichier texte avec retour à la ligne après chq pkg:
        places_libres_file.write(nom +', '+str(places_libres) + '\n')
    else :
        print(nom, statut)
        
# Fermeture du fichier de sortie
places_libres_file.close()

# In[6]: % places libres
"""
- écrire un programme qui donne le pourcentage de places libres
 pour chaque parking ainsi que le pourcentage de places libres 
 dans toute la ville.

"""
import json
# Ouverture du fichier json contenant les données sur les parkings
with open('data.json') as parking_file:
  parking_data = json.load(parking_file)

tot_places =0
taux_dispo =0
tot_dispo =0

for parking in parking_data:
  
    nom = parking['name']['value']
    # On récupère le nombre de places totales
    places_tot = parking['totalSpotNumber']['value']  
    
    # On récupère le nombre de places disponibles
    places_libres = parking['availableSpotNumber']['value'] 
    
    # On calcule le % de places dispo :
    taux_dispo = places_libres / places_tot *100
    tot_places = tot_places + places_tot
    tot_dispo= tot_dispo + places_libres
    print(nom, 'places_tot:',places_tot, 'places_libres:',places_libres, 'taux_dispo:',\
          round(taux_dispo,1))
        
tt_dispo = tot_dispo/tot_places*100
print()
print('Tot. ville : ', 'places_tot:',tot_places, 'places_libres:',tot_dispo, 'taux_dispo:',\
      round(tt_dispo,1))


# In[7]:  Etudier le programme suivant 
import time
temps = int(time.time()) 
print(temps)
"""Que représente le nombre obtenu ? 
Le nombre retourné par time.time() représente le temps écoulé (timestamp=horodatage) 
en secondes depuis le 1er janvier 1970 00:00:00 UTC,
également appelé Epoch UNIX.
Il permet de dater précisément un instant donné par rapport à cette origine"""


# In[8]:  Occupation au cours du temps  
"""
8)- Ecrire un programme qui permet de récupérer l’occupation du parking nommé « 
Corum » toutes les 10 secondes pendant 5 minutes et qui sauvegarde ces données 
dans un fichier.
"""
import requests
import time
import json

# durée en secondes : 
duree = 60*5 

output_file = open('occupation_corum.txt', 'w')

print('traitement en cours...')
for i in range(duree//10): # boucle de 10 s sur 5 mn

    response = requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    data = response.json()  
    
    print('period : ', i)
    for parking in data:
        nom = parking['name']['value']
        places_libres = parking['availableSpotNumber']['value']
        #time_register = parking['availableSpotNumber']['metadata']['timestamp']['value']
        
        if nom == 'Corum': 
            print(nom , i ,places_libres)
            #output_file.write(nom +', ' + str(i) +"," +str(places_libres) +'\n')
            output_file.write(f"{nom}, {str(i)}, {str(places_libres)}\n")
 # mise en pause 10 secondes :          
    time.sleep(10)

output_file.close()

# In[9]:suivi de l’occupation de tous les parkings 
"""
9)- Ecrire un programme qui permet le suivi de l’occupation de tous les parkings 
de Montpellier en permettant à l’utilisateur de choisir la période d’échantillonnage Te 
et la durée de l’acquisition. 
Il pourra également indiquer le nom du fichier dans lequel seront enregistrées les données.
"""

import requests
import json
import time


# Demander les paramètres à l'utilisateur : 
Te = int(input("Période d'échantillonnage (en secondes) ? : ")) 
duree = int(input("Durée de l'acquisition (en secondes) ? : "))
fichier = input("Nom du fichier de sortie : ? ")
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

# In[10] parking velos : 
import requests
import json
response=requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
dataV = response.json()
print(dataV)
