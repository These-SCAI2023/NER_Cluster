#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:16:20 2022

@author: antonomaz
"""


import numpy as np
from sklearn.cluster import AffinityPropagation
import distance
import json
import glob
import re
from collections import OrderedDict

def lire_fichier (chemin):
    with open(chemin) as json_data: 
        texte =json.load(json_data)
    return texte

def nomfichier(chemin):
    nomfich= chemin.split("/")[-1]
    nomfich= nomfich.split(".")
    nomfich= ("_").join([nomfich[0],nomfich[1]])
    return nomfich
    

def stocker(chemin,contenu):                                                    #definition fonction pour stocker fichier en format json
    w=open(chemin,"w")                                                          #ouverture du fichier en mode écriture
    w.write(json.dumps(contenu, indent=2))                                      #écriture du contenu dans le fichier
    w.close()  





path_copora = "../DATA/corpora_SPACY_CONCAT/*/*"
#path_copora = "../DATA/AIMARD_euclidean_damping09/*/*"


for subcorpus in glob.glob(path_copora):
#    print("SUBCORPUS***",subcorpus)
    liste_nom_fichier =[]
    for path in glob.glob("%s/*/*.json"%subcorpus):
#        print("PATH*****",path)
        
        nom_fichier = nomfichier(path)
#        print(nom_fichier)
        liste=lire_fichier(path)
##### FREQUENCE ########
        
        dic_mots={}
        i=0
        
        for mot in liste:
            if mot not in dic_mots:
                dic_mots[mot] = 1
            else:
                dic_mots[mot] += 1
                #dic_langues[langue][mot] = dic_langues[langue][mot] + 1
        
        i += 1
    #    print(dic_mots)
        new_d = OrderedDict(sorted(dic_mots.items(), key=lambda t: t[0]))
    
#        print(new_d)
#        freq=len(dic_mots.keys())
        
        Set_00 = set(liste)
        Liste_00 = list(Set_00)
        dic_output = {}
        i=0
        
        try:
            words = np.asarray(Liste_00) #So that indexing with a list will work
            lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])
            
            affprop = AffinityPropagation(affinity="precomputed", damping= 0.9, random_state = None)
#            affprop = AffinityPropagation(affinity="precomputed", damping= 0.5, random_state = None) 
            affprop.fit(lev_similarity)
            for cluster_id in np.unique(affprop.labels_):
                exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
                cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
                cluster_str = ", ".join(cluster)
                cluster_list = cluster_str.split(", ")
#                print(" - *%s:* %s" % (exemplar, cluster_str))                
                Id = "ID "+str(i)
                for cle, dic in new_d.items(): 
                    if cle == exemplar:
                        dic_output[Id] ={}
                        dic_output[Id]["Centroïde"] = exemplar
                        dic_output[Id]["Freq. centroide"] = dic
                        dic_output[Id]["Termes"] = cluster_list
                
                i=i+1
            stocker("%s/%s_cluster_damping-09.json"%(subcorpus,nom_fichier),dic_output)
        except :
            
            print("**********Non OK***********", path)
            liste_nom_fichier.append(path)
            stocker("%s/fichier_non_cluster_damping-09.json"%subcorpus, liste_nom_fichier)
            
            continue 
   
#entite =  lire_fichier("../DATA/AIMARD-TRAPPEURS/AIMARD-TRAPPEURS_kraken-base/AIMAR-TRAPPEURS_REF/AIMARD_les-trappeurs_REF.txt_lg_spacy.json-concat.json")   
##words = "YOUR WORDS HERE".split(" ") #Replace this line
#print(len(entite))
#entite= set(entite)
#print(len(entite))
#entite=list(entite)
#words = np.asarray(entite) #So that indexing with a list will work
#lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])
#
#affprop = AffinityPropagation(affinity="precomputed", damping=0.5)
#affprop.fit(lev_similarity)
#for cluster_id in np.unique(affprop.labels_):
#    exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
#    cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
#    cluster_str = ", ".join(cluster)
#    print(" - *%s:* %s" % (exemplar, cluster_str))   
    


    
    

        
        
          