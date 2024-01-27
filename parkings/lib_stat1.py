# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 22:13:37 2024

@author: franc
"""

import datetime
import re
from statistics import mean
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt 
 
def stat_1(data):
    # Appel de la fonction de calcul
    resultats = calcul_moyennes(data)  

    # Affichage des résultats
    print("Moyennes par mois:")
    print(resultats['mois'])

    print("Moyennes par semaine:") 
    print(resultats['semaine'])

    print("Moyennes par jour de semaine:") 
    print(resultats['jour_semaine'])
        
    print("Moyennes par jour:")
    print(resultats['jour'])

    print("Moyennes par heure:")
    print(resultats['heure'])

    return resultats


def test_timestamp(ts):
    timestamp_regex = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{2}:\d{2}'
    if not re.match(timestamp_regex, ts):
        print(f"Timestamp incorrect: {ts}")
        return False
    return True

def calcul_moyennes(data):
    
    agregats = {
        'mois': {},
        'semaine': {}, 
        'jour': {},
        'heure': {},
        'jour_semaine': {} 
    }
    
    timestamps = data['index']
    values = data['values']
    
    for ts, val in zip(timestamps, values):
        #print(ts, val)
        if not test_timestamp(ts):
            continue
            
        dt = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f%z')
        
        key_mois = f"{dt.year}-{dt.month}"
        key_sem = f"{dt.year}-{dt.strftime('%W')}"
        key_jour = f"{dt.year}-{dt.month}-{dt.day}" 
        key_heure = f"{dt.hour}"
        key_jour_sem = dt.strftime('%A') 

        agregats['mois'].setdefault(key_mois, []).append(val)
        agregats['semaine'].setdefault(key_sem, []).append(val)
        agregats['jour'].setdefault(key_jour, []).append(val)
        agregats['heure'].setdefault(key_heure, []).append(val)
        agregats['jour_semaine'].setdefault(key_jour_sem, []).append(val)          
        
    for periode, values in agregats.items():
        for k, v in values.items():      
            values[k] = round(mean(v),1)

    
    
    # graphique par semaine : 
    semaines = list(agregats['semaine'].keys())
    moyennes = list(agregats['semaine'].values()) 
    
    fig, ax = plt.subplots()
    
    sns.barplot(x=semaines, y=moyennes)
    
    ax.set_xlabel("Semaine")
    ax.set_ylabel("Valeur moyenne")
    ax.set_title("Moyennes par semaine")
    
    plt.savefig("semaines.png")

    plt.show()

  
    # graphique par jour de semaine : 
    jour_semaine = list(agregats['jour_semaine'].keys())
    moyennes = list(agregats['jour_semaine'].values()) 
    
    fig, ax = plt.subplots()
    
    sns.barplot(x=jour_semaine, y=moyennes)
    
    ax.set_xlabel("jour de Semaine")
    ax.set_ylabel("Valeur moyenne")
    ax.set_title("Moyennes par jour de semaine")
    
    plt.savefig("jour_semaine.png")

    plt.show()


    # graphique par jour : 
    jour = list(agregats['jour'].keys())
    moyennes = list(agregats['jour'].values()) 
    
    fig, ax = plt.subplots()
   
    sns.barplot(x=jour, y=moyennes)
    
    ax.set_xlabel("jour")
    ax.set_ylabel("Valeur moyenne")
    ax.set_title("Moyennes par jour")
    
    plt.savefig("jour.png")

    plt.show()
    
    

# Graphiques distribution (nombre d'unités (jour, heure, ..) par valeur de nb de véhicules)

    fig, axs = plt.subplots(2, 2, figsize=(10,8))

    sns.histplot(agregats['mois'].values(), bins=20, ax=axs[0,0])
    axs[0,0].set_title('Moyennes par mois')

    sns.histplot(agregats['semaine'].values(), bins=20, ax=axs[0,1]) 
    axs[0,1].set_title('Moyennes par semaine')

    sns.histplot(agregats['jour'].values(), bins=20, ax=axs[1,0])
    axs[1,0].set_title('Moyennes par jour')

    sns.histplot(agregats['heure'].values(), bins=20, ax=axs[1,1])
    axs[1,1].set_title('Moyennes par heure')

    plt.tight_layout()
    plt.show()
  
    return agregats