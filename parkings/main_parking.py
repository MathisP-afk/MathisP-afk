# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 19:33:37 2024

@author: franc
"""
# In[0] :repertoire de travail :
import os
#dir_pkg = "D:\\Documents\\Mathis\IUT\Année_1\\informatique\parkings2"
dir_pkg ='D:\Documents\\admin\Mathis\IUT\\année_1\Informatique\parkings2'
os.chdir(dir_pkg)


# In[1] : import librairie parking :
import lib_parking
import lib_velo
import lib_stat1
import lib_stat2
import lib_stat3

# In[2] : importation base parking :
""" source : api https://portail-api-data.montpellier3m.fr/offstreetparking
indiquer la période d'échantillonnage
la duree et le nom du fichier """

Te = 2
duree = 60
fichier = 'test.txt'

parking_time(Te, duree, fichier)

# In[3] : importation base velo :
""" source : https://portail-api-data.montpellier3m.fr/bikestation
indiquer la période d'échantillonnage
la duree et le nom du fichier """

Te = 2
duree = 60
fichier = 'test.txt'

velo_time(Te, duree, fichier)

# In[4] : récupération des ID parking :
""" source : api https://portail-api-data.montpellier3m.fr/parkingspaces
renvoi la liste des parkings et l'ID parking
pour pouvoir interroger la base historique
"""
list_pkg = list_pkg() 
print(list_pkg)

# In[5] : récupération des ID velos :
""" source : api https://portail-api-data.montpellier3m.fr/bikestation
renvoi la liste des parkings vlo et l'ID parking
pour pouvoir interroger la base historique
"""
list_velo = list_velo() 
print(list_velo)

# In[6] : récupération de l'ID du parking a étudié :
nom_P = 'Gaumont EST'
id_P = ID_pkg(nom_P)
print(id_P, nom_P)

# In[7] : récupération de l'ID du park velo a étudié :
nom_V = 'Corum'
id_V = ID_velo(nom_V)
print(id_V, nom_V)
    
# In[8] : importation API base historique parking pour 1 parking donné :
""" source : api https://portail-api-data.montpellier3m.fr/parking_timeseries/{parkingId}/attrs/avai1ab1eSpotNumber
récupération de la base historique à partir de l'ID récupé prédemment [6]"""
#from_date = "2023-01-01" 
from_date = "2024-01-01" 
to_date = "2024-01-14" 

dhisto_pkg = histo_pkg(id_P, nom_P, from_date, to_date)

# In[9] : importation API base historique parking pour l'ensemble des parkings :
""" source : api https://portail-api-data.montpellier3m.fr/parking_timeseries/{parkingId}/attrs/avai1ab1eSpotNumber
récupération de la base historique à partir de l'ID récupé dans fichier ID_P """
from_date = "2023-01-01" 
to_date = "2023-12-31" 
histo_pkg_global(from_date, to_date)

# In[10] : importation API base historique de tous les parkings avec 1 fichier par parking :
""" source : api https://portail-api-data.montpellier3m.fr/parking_timeseries/{parkingId}/attrs/avai1ab1eSpotNumber
récupération de la base historique de chaque pkg"""
from_date = "2023-01-01" 
to_date = "2023-12-31" 
histo_pkgT(from_date, to_date)


# In[11] : importation API base historique velos pour 1 park_velo donné :
""" source : api https://portail-api-data.montpellier3m.fr/bikestation_timeseries/{bikeStationId}/attrs/avai1ab1eBikeNumber    
récupération de la base historique à partir de l'ID récupé prédemment [7]"""
from_date = "2023-12-01" 
to_date = "2023-12-31" 

#dhisto_velo = histo_velo(id_V, nom_V, from_date, to_date)
dhisto_velo = histo_velo2(id_V, nom_V, from_date, to_date)


# In[12] : importation API base historique de tous les parks velos avec 1 fichier par park velo :
""" source : api https://portail-api-data.montpellier3m.fr/bikestation_timeseries/{bikeStationId}/attrs/avai1ab1eBikeNumber    
récupération de la base historique à partir de l'ID base station [id_velo]"""
from_date = "2023-01-01" 
to_date = "2023-12-31" 

#histo_veloT(from_date, to_date)
histo_veloT2(from_date, to_date)

# In[13] : importation API base historique park velo pour l'ensemble des parks :
""" source : api https://portail-api-data.montpellier3m.fr/bikestation_timeseries/{bikeStationId}/attrs/avai1ab1eBikeNumber    
récupération de la base historique à partir de l'ID base station [id_velo]"""
from_date = "2023-01-01" 
to_date = "2023-12-31" 
histo_velo_global(from_date, to_date)

# In[14] : importation FIC base historique d'un parking avec 1 fichier par parking :
""" 
récupération de la base historique d'un pkg préalablement enregistré sur disque """
nom_P= 'Vicarello'
data_E = imp_fic_histo(nom_P)

# In[15] : importation FIC base historique d'un park velo avec 1 fichier par park :
""" 
récupération de la base historique d'un park velo préalablement enregistré sur disque """
nom_V= 'Corum'
data_F = velo_fic_histo(nom_V)

# In[15] : traitement statistique d'un parking :
""" 
statistiques du parking par : mois, année, jour, heure
du data chargé (depuis DD) [14]
"""
base_agreg = stat_1(data_E)
print(base_agreg)
# In[16] : calcul du nbr heures, jours dont le nbr de places occupées > seuil (ex 90 % capacité max) :
nom_P= 'Antigone'
id_P = ID_pkg(nom_P)
print(id_P, nom_P)
capacity = get_capacity(id_P)
taux = 0.9
seuil = capacity * taux
print("capacity", capacity)

# récupération de la base historique d'un pkg préalablement enregistré sur disque :

data_E = imp_fic_histo(nom_P)
comptage_depassement(data_E, seuil)

# In[17]] : charge base parking, velo : 
#fic= 'ID_pkg2.json'
fic= 'ID_pkg.json'
ID_PKG = charge_ID_pkg(fic)
    
fic= 'ID_velo.json'
ID_velo = charge_ID_velo(fic)
    

# In[17] : calcul du nbr heures, jours dont le nbr de places occupées > seuil (ex 90 % capacité max) : POUR TOUTES LES STATIONS
#nom_P = 'Corum'
#id_P = ID_pkg(nom_P)
#print(id_P, nom_P)
#capacity = get_capacity(id_P)
taux = 0.9
#seuil = capacity * taux
#print("capacity", capacity)

# récupération de la base historique d'un pkg préalablement enregistré sur disque :
#nom_P= 'Corum'
#data_E = imp_fic_histo(nom_P)
comptage_depassement_pkgT(taux)

# In[18] : 
nom_P= 'Antigone'
base = 'histo_'+nom_P+'.json'
test_base(base)

# In[19] : 
trait_compl_pkg() 

#trait_compl_velo()
trait_compl_velo2()

# In[20] : 
verif_pkg() 
verif_velo()      

# In[20] : 

idP = 'urn:ngsi-ld:parking:019'
nomP = 'Vicarello'
trait_pkg(idP, nomP) 

# In[21]:
genere_dataframe_pkg()  
