# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 11:55:32 2024

@author: FlowUp
"""
import os
import json
import datetime
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

"""Génère des dataframes de Pandas pour chaque parking.
"""
pd.set_option('display.max_columns', None)    
plt.figure(dpi=150)   

rep_base= os.getcwd()
rep = rep_base + '\Data_frame\parking\jours'

if not os.path.exists(rep):
  os.makedirs(rep)
else:
    print(os.getcwd()+rep)

#print('repertoire courant', os.getcwd()+rep)  
#ss = input('stop')

# boucle sur les parkings :
    

# ID_pkg2.json (source sans 2 pkgs Gaumont vides)
with open('json/ID_pkg2.json') as file: list_pkg = json.load(file)
for parking in list_pkg:
    # init :

    idP = parking['id']
    code_idP = idP[-3:]
    nomP = parking['name']['value']
    capacite_max = parking['totalSpotNumber']['value'] 
    seuil = capacite_max * 0.9
    print(capacite_max)
    fic = 'json/histo_' + nomP + '.json'
  
    
    with open(fic) as parking_file:
        pkg_data = json.load(parking_file)
        
    timestamps = np.array(pkg_data["index"])
    values = np.array(pkg_data["values"])
    capacite_max = parking['totalSpotNumber']['value']
    seuil = capacite_max * 0.9

    df = pd.DataFrame({'timestamp': timestamps, 'values': values})

    df['jour'] = df['timestamp'].dt.weekday
  
    jours = [0,1,2,3,4,5,6]
    Name_jours = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dataF_comp = pd.DataFrame(columns=['jour'])  
    dataF_comp["jour"] = jours
    dataF_comp["N_jour"] = Name_jours
    dataF_comp.set_index('jour',inplace=True)
  
    ss = input('stop')
  

    # Grouper par jour de semaine
    df_grp = df.groupby('jour')[['values']].agg({
    'values': ['size', 'min', 'max', 'mean', 'std', 'sum']
    })

    # Ajouter les données groupées 
    #dataF_comp = dataF_comp.join(df_grp)
    #dataF_comp = dataF_comp.join(df_grp, on='jour')
    dataF_comp = dataF_comp.join(df_grp, left_index=True, right_index=True) 
    print(dataF_comp)
    
    ss = input('stop')
    
    # Calcule les autres statistiques
   
    dataF_comp["Q1"] = df.groupby("jour")["values"].quantile(0.25) 
    dataF_comp["median"] = df.groupby("jour")["values"].median()
    dataF_comp["Q3"] = df.groupby("jour")["values"].quantile(0.75)
    
    
    # Compter directement le nb de valeurs > seuil 
    dataF_comp["nb_sup_seuil"] = df.groupby("jour")["values"].transform(lambda x: (x>seuil).sum())
   
    
    # Calcul du taux d'occupation dans le dataframe source
    df["taux_occ"] = (df["values"] / capacite_max)* 100  
    # Aggregation dans le dataframe traité
    dataF_comp["taux_occ"] = df.groupby("jour")[["taux_occ"]].agg({
    "taux_occ": "mean"})
    ss = input('stop')

    print(dataF_comp.head())
    #fic = 'json/histo_' + nomP + '.json'
    fic_svg = rep + '/data_f_' + code_idP+'-'+ nomP + '.csv'
    fic_gp1 = rep + '/mean_'+ code_idP +'-' + nomP + '.png'
    
    print(fic_svg)
    dataF_comp.to_csv(fic_svg, index=False, encoding='utf-8', sep=';')    
    
    # graphiques: 
     
    # GRAPHIQUE min, max, moy :
    plt.title(code_idP+'-'+nomP)
    maxy = dataF_comp['max'].max()*1.5
    plt.ylim(0, maxy)
        
    plt.errorbar(dataF_comp['hour'], dataF_comp['mean'], yerr=[dataF_comp['mean'] - dataF_comp['min'], dataF_comp['max'] - dataF_comp['mean']], fmt='o', color='black', ecolor='grey', capsize=5, label='min, moy. max')
    plt.legend(loc='lower left')
    plt.savefig(fic_gp1)
    plt.show()
    
    # GRAPHIQUE médiane, Q1, Q3 :
                  
    # Tracer la ligne pour la médiane
    # Démarrer l'échelle y à 0
    plt.figure(dpi=150)   
    maxy = dataF_comp['Q3'].max()*1.5
    plt.ylim(0, maxy)
    sns.lineplot(data=dataF_comp, x="hour", y='median')
    
       
    # Tracer la zone d'incertitude avec les quartiles  
    sns.lineplot(data=dataF_comp, x="hour", y='Q1', color= 'grey')
    sns.lineplot(data=dataF_comp, x="hour", y='Q3', color= 'grey')
    #sns.lineplot(data=dataF_comp, x="hour", y=quartiles, color="grey", linewidth=1,legend=False)
    plt.fill_between(dataF_comp['hour'], dataF_comp['Q1'], dataF_comp['Q3'], color='grey', alpha=0.2)
    
    plt.title(code_idP+'-'+nomP)
    # Afficher la legende
    plt.plot([], [], color='grey', label='Intervalle interquartile')
    plt.legend(loc='lower left')
    fic_gp2 = rep + '/median_'+ code_idP +'-' + nomP + '.png'
    plt.savefig(fic_gp2)
    plt.show()   
    
    # GRAPHIQUE Taux d'Occupation :
    plt.figure(dpi=150)    
    plt.title(code_idP+'-'+nomP)
    ax = sns.barplot(x="hour", y="taux_occ", data=dataF_comp)
    # Accédez aux barres individuelles dans le graphique
    for i, bar in enumerate(ax.patches):
        # Vérifiez la condition et définissez la couleur en conséquence
        if dataF_comp['taux_occ'][i] > 90:
            bar.set_facecolor((1, 0, 0, 0.5))  # Rouge pastel avec opacité de 0.5
        else:
            bar.set_facecolor((0, 0, 1, 0.5))  # Bleu pastel avec opacité de 0.5    # Accédez aux barres individuelles dans le graphique
                
    
    fic_gp3 = rep + '/T_Occup_'+ code_idP +'-' + nomP + '.png'
    plt.savefig(fic_gp3)
    plt.show()        

    ss = input('stop')
