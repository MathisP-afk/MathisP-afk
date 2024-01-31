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

"""Génère des dataframes de Pandas pour chaque park.
"""
pd.set_option('display.max_columns', None)    
  

rep_base= os.getcwd()
rep = rep_base + '\Data_frame\\velo\jour'

if not os.path.exists(rep):
  os.makedirs(rep)
else:
    print(os.getcwd()+rep)

#print('repertoire courant', os.getcwd()+rep)  
#ss = input('stop')

# boucle sur les parks :
    
with open('json/ID_velo.json') as file: list_pkg = json.load(file)

for park in list_pkg:
    # init :

    idP = park['id']
    code_idP = idP[-3:]
    nomV = park['address']['value']['streetAddress']
    capacite_max = park['totalSlotNumber']['value'] 
    
    print(capacite_max)
    fic = 'json/histoVelo_' + nomV + '.json'  
    
    with open(fic) as park_file:
        pkg_data = json.load(park_file)

    #timestamps = pkg_data['index']
    #values = pkg_data['values']
    #convert the lists timestamps and values into a hashable data structure before creating the DataFrame.
    timestamps = np.array(pkg_data["index"])
    values = np.array(pkg_data["values"])

    data = {"timestamp": timestamps, "values": values}
    dataframe = pd.DataFrame(data)

    # filtre des valeurs dont le comptage > Seuil : 
    # Supprimer les lignes où les valeurs dépassent la capacité maximum 
    dataframe = dataframe[(dataframe['values'] <= capacite_max)]


    # Reformate le timestamp (supprime notamment le 'T')
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])     
    print(dataframe.dtypes)
    #print(dataframe["timestamp"].dt.hour)
    dataframe["jour"] = dataframe["timestamp"].dt.dayofweek
    
    dataframe['penurie'] = dataframe['values'].apply(lambda x: 1 if x == 0 else 0)
    
    dataF_comp = pd.DataFrame(columns=["jour"])     
    # Calcul du jour : 
    

    # Créer le dataframe d'heures vides
    jours = list(range(7))
    nameJ = ['Mon', 'Tues', 'Wed','Thur', 'Fri', 'Sat', 'Sun']
    #dataF_comp = pd.DataFrame(columns=["hour"]) 
    dataF_comp["jour"] = jours
    dataF_comp["jours"] = nameJ
    
   
    # Calcule les statistiques
    dataF_comp["nb_data"] = dataframe.groupby("jour")["values"].count()
    dataF_comp["min"] = dataframe.groupby("jour")["values"].min()
    dataF_comp["max"] = dataframe.groupby("jour")["values"].max()
    dataF_comp["mean"] = round(dataframe.groupby("jour")["values"].mean(),1)
    dataF_comp["std"] = round(dataframe.groupby("jour")["values"].std(),1)
    dataF_comp["sum"] = dataframe.groupby("jour")["values"].sum()
    dataF_comp["Q1"] = dataframe.groupby("jour")["values"].quantile(0.25) 
    dataF_comp["median"] = dataframe.groupby("jour")["values"].median()
    dataF_comp["Q3"] = dataframe.groupby("jour")["values"].quantile(0.75)
    
    
    # Calcul du taux d'occupation dans le dataframe source
    dataframe["taux_dispo"] = (dataframe["values"] / capacite_max)* 100  
    # Aggregation dans le dataframe traité
    dataF_comp["taux_dispo"] = round(dataframe.groupby("jour")[["taux_dispo"]].agg({
    "taux_dispo": "mean"}),2)
    
    dataF_comp["taux_occ"] = 100- dataF_comp["taux_dispo"] 

    # Compter le nb de valeurs = 0  (Penurie) :
    dataF_comp["penurie"] = dataframe.groupby("jour")["penurie"].sum()    
    # Calcul du taux de pénurie dans le dataframe source
    dataF_comp["taux_penurie"] = (dataF_comp["penurie"] / dataF_comp["nb_data"])* 100  

    # Calcul du taux d'occupation dans le dataframe source
    dataframe["taux_occ"] = (dataframe["values"] / capacite_max)* 100  
    
    
    
    print(dataF_comp.head())
    #fic = 'json/histo_' + nomP + '.json'
    fic_svg = rep + '/data_f_' + code_idP+'-'+ nomV + '.csv'
    fic_gp1 = rep + '/mean_'+ code_idP +'-' + nomV + '.png'
    
    print(fic_svg)
    dataF_comp.to_csv(fic_svg, index=False, encoding='utf-8', sep=';')    
    
    # graphiques: 
     
    # GRAPHIQUE min, max, moy :
    plt.title(code_idP+'-'+nomV)
    maxy = dataF_comp['max'].max()*1.5
    plt.ylim(0, maxy)
        
    plt.errorbar(dataF_comp['jours'], dataF_comp['mean'], yerr=[dataF_comp['mean'] - dataF_comp['min'], dataF_comp['max'] - dataF_comp['mean']], fmt='o', color='black', ecolor='grey', capsize=5, label='min, moy. max')
    plt.legend(loc='lower left')
    plt.savefig(fic_gp1)
    plt.show()
    
    # GRAPHIQUE médiane, Q1, Q3 :
                  
    # Tracer la ligne pour la médiane
    # Démarrer l'échelle y à 0
    plt.figure(dpi=150)   
    maxy = dataF_comp['Q3'].max()*1.5
    plt.ylim(0, maxy)
    sns.lineplot(data=dataF_comp, x="jours", y='median')
    
       
    # Tracer la zone d'incertitude avec les quartiles  
    sns.lineplot(data=dataF_comp, x="jours", y='Q1', color= 'grey')
    sns.lineplot(data=dataF_comp, x="jours", y='Q3', color= 'grey')
    #sns.lineplot(data=dataF_comp, x="hour", y=quartiles, color="grey", linewidth=1,legend=False)
    plt.fill_between(dataF_comp['jours'], dataF_comp['Q1'], dataF_comp['Q3'], color='grey', alpha=0.2)
    
    plt.title(code_idP+'-'+nomV)
    # Afficher la legende
    plt.plot([], [], color='grey', label='Intervalle interquartile')
    plt.legend(loc='lower left')
    fic_gp2 = rep + '/median_'+ code_idP +'-' + nomV + '.png'
    plt.savefig(fic_gp2)
    plt.show()   

    # GRAPHIQUE Taux de disponibilité :
    plt.figure(dpi=150)
    plt.title(code_idP+'-'+nomV)

    ax = sns.barplot(x="jours", y="taux_dispo", data=dataF_comp, color='green')
   
    fic_gp3 = rep + '/T_Dispo_'+ code_idP +'-' + nomV + '.png'
    plt.savefig(fic_gp3)
    plt.show()      

   
    # GRAPHIQUE Taux d'Occupation :
    plt.figure(dpi=150)    
    plt.title(code_idP+'-'+nomV)
    ax = sns.barplot(x="jours", y="taux_occ", data=dataF_comp)
    # Accédez aux barres individuelles dans le graphique
    for i, bar in enumerate(ax.patches):
        # Vérifiez la condition et définissez la couleur en conséquence
        if dataF_comp['taux_occ'][i] > 90:
            bar.set_facecolor((1, 0, 0, 0.5))  # Rouge pastel avec opacité de 0.5
        else:
            bar.set_facecolor((0, 0, 1, 0.5))  # Bleu pastel avec opacité de 0.5    # Accédez aux barres individuelles dans le graphique
                
    
    fic_gp4 = rep + '/T_Occup_'+ code_idP +'-' + nomV + '.png'
    plt.savefig(fic_gp4)
    plt.show()        


    # GRAPHIQUE Taux de Pénurie :
    plt.figure(dpi=150)    
    plt.title(code_idP+'-'+nomV)
    ax = sns.barplot(x="jours", y="taux_penurie", data=dataF_comp)
    fic_gp5 = rep + '/T_Penurie_'+ code_idP +'-' + nomV + '.png'
    plt.savefig(fic_gp5)    
    plt.show()

    #ss = input('stop')
