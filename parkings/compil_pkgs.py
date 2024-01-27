# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 09:46:55 2024

@author: Mathis
compialtion base parkings

"""
# In[1]: init bases :
    
import os
import pandas as pd
import numpy as np
import json

pd.set_option('display.max_columns', None)    

rep_base= os.getcwd()
print(rep_base)
rep = rep_base + '\Data_frame\parking\compil'

if not os.path.exists(rep):
  os.makedirs(rep)
else:
    print(os.getcwd()+rep)



def charge_DF(rep, code_idP, nomP):

    fic_imp = rep + '/data_f_' + code_idP+'-'+ nomP + '.csv'
    return pd.read_csv(fic_imp, sep=';')



def stats_H(ind, idP, nom, bdd, d_G):
   
    nuit_occ = round(bdd['taux_occ'].iloc[0:7].mean(),2)        
    jour_occ = round(bdd['taux_occ'].iloc[8:17].mean(),2)        
    soir_occ = round(bdd['taux_occ'].iloc[18:23].mean(),2)        
    d = {'id': idP,'nom': nom, 'nuit_occ':nuit_occ, 'jour_occ':jour_occ, 'soir_occ':soir_occ}
    if ind == 0:
        # creation du dataframe à partir du dico
        d_G = pd.DataFrame(d, index=[ind])
    else:
        #_G = d_G.append(d, ignore_index=True)
        # Ajoutez le dictionnaire au dataframe
       
        d2 = pd.DataFrame(d, index=[ind])
        d_G = pd.concat([d_G, d2], ignore_index=True)
       
    print(ind)
    return d_G

def stats_J(ind, idP, nom, bdd, d_G):
   
    sem_occ = round(bdd['taux_occ'].iloc[0:5].mean(),2)        
    we_occ = round(bdd['taux_occ'].iloc[6:7].mean(),2)
    tx_occ =round(bdd['taux_occ'].mean(),2)         
    Tx_penurie = round(bdd['taux_penurie'].mean(),2)
    
    #création des nouvelles colonnes du DF : 
    if ind == 0:
       
        d_G['sem_occ'] = np.nan
        d_G['we_occ'] = np.nan
        d_G['tx_occ'] = np.nan
        d_G['tx_penurie'] = np.nan
        
    # remplissage
    d_G.loc[ind,'sem_occ'] = sem_occ
    d_G.loc[ind,'we_occ'] = we_occ
    d_G.loc[ind,'tx_occ'] = tx_occ
    d_G.loc[ind,'tx_penurie'] = Tx_penurie
        
    print(ind)
    return d_G


def stats_M(ind, idP, nom, bdd, d_G):
   
   # été = juil, aout 
   ete_occ = round(bdd['taux_occ'].iloc[6:7].mean(),2)        
   autsaison_occ1 = round(bdd['taux_occ'].iloc[0:5].mean(),2)        
   autsaison_occ2 = round(bdd['taux_occ'].iloc[8:11].mean(),2)        
   autsaison_occ = round((autsaison_occ1 *6+ autsaison_occ2*4)/10,2)
   
   #création des nouvelles colonnes du DF :
   if ind == 0:
       d_G['ete_occ'] = np.nan
       d_G['autsaison_occ'] = np.nan
        
   # remplissage
   d_G.loc[ind,'ete_occ'] = ete_occ
   d_G.loc[ind,'autsaison_occ'] = autsaison_occ
       
   print(ind)
   return d_G




# ID_pkg2.json (source sans 2 pkgs Gaumont vides)
with open('json/ID_pkg2.json') as file: list_pkg = json.load(file)

# Lecture du fichier zones 
dfzone = pd.read_csv(rep+'\zone_parkings.csv', sep=';',encoding='utf-8')
                  
                  
d_G = pd.DataFrame()
ind = 0

for parking in list_pkg:
    # init :
            
    idP = parking['id']
    code_idP = idP[-3:]
    nomP = parking['name']['value']
    nom = code_idP +"-"+nomP
    repH = rep = rep_base + '\Data_frame\parking\heure'
    bdd = charge_DF(repH, code_idP, nomP)
    d_G = stats_H(ind, code_idP, nom, bdd, d_G)
    print(d_G['nuit_occ'])
    
    repJ = rep = rep_base + '\Data_frame\parking\jour'
    bdd2 = charge_DF(repJ, code_idP, nomP)
    d_G = stats_J(ind, code_idP, nom, bdd2, d_G)
    print(d_G['sem_occ'])

    repM = rep = rep_base + '\Data_frame\parking\mois'
    bdd3 = charge_DF(repM, code_idP, nomP)
    d_G = stats_M(ind, code_idP, nom, bdd3, d_G)
    print(d_G['ete_occ'])    
    
    
    ind = ind+1
    d_G['zone']=dfzone['zone']
    #ss = input('stop')



rep = rep_base + '\Data_frame\\parking\compil'
fic_svg = rep + '/parkings.txt'
fic_xls = rep + '/parkings.xlsx'
   
print(fic_svg)
d_G.to_csv(fic_svg, index=False, encoding='utf-8', sep=';')    

# Sauver le dataframe dans un fichier Excel
d_G.to_excel(fic_xls, index=False)

    
# In[2]: interrogation base : 
## interrogation de la base :
#Query =  'tx_penurie>0'
#Query =  'we_occ > 50 and tx_penurie>0'
#Query =  'we_occ > sem_occ * 0.9'
Query =  'zone == "Centre"'

print(d_G.query(Query))    

## nouveaux calculs sur la base : 
param='we_occ'
print(d_G.query(Query)[param].mean())
