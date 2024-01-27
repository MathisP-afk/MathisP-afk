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
rep = rep_base + '\Data_frame\\velo\compil'

if not os.path.exists(rep):
  os.makedirs(rep)
else:
    print(os.getcwd()+rep)



def charge_DF(rep, code_idV, nomV):

    fic_imp = rep + '/data_f_' + code_idV+'-'+ nomV + '.csv'
    return pd.read_csv(fic_imp, sep=';')




def stats_H(ind, idV, nom, bdd, d_V):
   
    nuit_occ = round(bdd['taux_occ'].iloc[0:7].mean(),2)        
    jour_occ = round(bdd['taux_occ'].iloc[8:17].mean(),2)        
    soir_occ = round(bdd['taux_occ'].iloc[18:23].mean(),2)        
    d = {'id': idV, 'nom': nom, 'nuit_occ':nuit_occ, 'jour_occ':jour_occ, 'soir_occ':soir_occ}
    if ind == 0:
        # creation du dataframe à partir du dico
        d_V = pd.DataFrame(d, index=[ind])
    else:
        #d_V = d_V.append(d, ignore_index=True)
        # Ajoutez le dictionnaire au dataframe

        d2 = pd.DataFrame(d, index=[ind])
        d_V = pd.concat([d_V, d2], ignore_index=True)
       
    print(ind)
    return d_V

def stats_J(ind, idV, nom, bdd, d_V):
   
    sem_occ = round(bdd['taux_occ'].iloc[0:5].mean(),2)        
    we_occ = round(bdd['taux_occ'].iloc[6:7].mean(),2)        
    tx_occ = round(bdd['taux_occ'].mean(),2)        
    Tx_penurie = round(bdd['taux_penurie'].mean(),2)
    
    #création des nouvelles colonnes du DF : 
    if ind == 0:
       
        d_V['sem_occ'] = np.nan
        d_V['we_occ'] = np.nan
        d_V['tx_occ'] = np.nan
        d_V['tx_penurie'] = np.nan
        
    # remplissage
    d_V.loc[ind,'sem_occ'] = sem_occ
    d_V.loc[ind,'we_occ'] = we_occ
    d_V.loc[ind,'tx_occ'] = tx_occ
    d_V.loc[ind,'tx_penurie'] = Tx_penurie
        
    print(ind)
    return d_V


def stats_M(ind, idV, nom, bdd, d_V):
   
   # été = juil, aout 
   ete_occ = round(bdd['taux_occ'].iloc[6:7].mean(),2)        
   autsaison_occ1 = round(bdd['taux_occ'].iloc[0:5].mean(),2)        
   autsaison_occ2 = round(bdd['taux_occ'].iloc[8:11].mean(),2)        
   autsaison_occ = round((autsaison_occ1 *6+ autsaison_occ2*4)/10,2)
   
   #création des nouvelles colonnes du DF :
   if ind == 0:
       d_V['ete_occ'] = np.nan
       d_V['autsaison_occ'] = np.nan
        
   # remplissage
   d_V.loc[ind,'ete_occ'] = ete_occ
   d_V.loc[ind,'autsaison_occ'] = autsaison_occ
       
   print(ind)
   return d_V



# ID_pkg2.json (source sans 2 pkgs Gaumont vides)
with open('json/ID_velo.json') as file: list_velo = json.load(file)

# Lecture du fichier zones 
dfzone = pd.read_csv(rep+'\zone_velos.csv', sep=';',encoding='utf-8')
                  
                  
d_V = pd.DataFrame()
ind = 0

for park in list_velo:
    # init :
            
    idV = park['id']
    code_idV = idV[-3:]
    nomV = park['address']['value']['streetAddress']
    nom = code_idV +"-"+nomV
    repH = rep = rep_base + '\Data_frame\\velo\heure'
    bdd = charge_DF(repH, code_idV, nomV)
    d_V = stats_H(ind, code_idV, nom, bdd, d_V)
    print(d_V['nuit_occ'])
    
    repJ = rep = rep_base + '\Data_frame\\velo\jour'
    bdd2 = charge_DF(repJ, code_idV, nomV)
    d_V = stats_J(ind, code_idV, nom, bdd2, d_V)
    print(d_V['sem_occ'])

    repM = rep = rep_base + '\Data_frame\\velo\mois'
    bdd3 = charge_DF(repM, code_idV, nomV)
    d_V = stats_M(ind, code_idV, nom, bdd3, d_V)
    print(d_V['ete_occ'])    
    
    
    ind = ind+1
    d_V['zone']=dfzone['zone']
    #ss = input('stop')
rep = rep_base + '\Data_frame\\velo\compil'
fic_svg = rep + '//velos.txt'
fic_xls = rep + '//velos.xlsx'

   
print(fic_svg)
d_V.to_csv(fic_svg, index=False, encoding='utf-8', sep=';')    

# Sauver le dataframe dans un fichier Excel
d_V.to_excel(fic_xls, index=False)

    
# In[2]: interrogation base : 
## interrogation de la base :
#Query =  'tx_penurie>0'
#Query =  'we_occ > 50 and tx_penurie>0'
#Query =  'we_occ > sem_occ * 0.9'
Query =  'zone == "Centre"'

print(d_V.query(Query))    
## nouveaux calculs sur la base : 

param='we_occ'
print(d_V.query(Query)[param].mean())
