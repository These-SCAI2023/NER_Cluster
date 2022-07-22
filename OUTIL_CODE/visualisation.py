#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 15:41:37 2022

@author: antonomaz
"""


import matplotlib.pyplot as plt
import json
import glob

def lire_fichier (chemin):
    with open(chemin) as json_data: 
        texte =json.load(json_data)
    return texte

def nomfichier(chemin):
    nomfich= chemin.split("/")[-1]
    nomfich= nomfich.split(".")
    nomfich= ("_").join([nomfich[0]])
    return nomfich

def stocker_graph(nomfich): 
    
    name_fig = "%s.png"
    print(" nom de la figure ", name_fig)
#    
    plt.legend(loc="lower left",ncol=2, bbox_to_anchor=(-0.05,0.98))
    plt.legend 
    
    plt.savefig(nomfich, figsize=(200, 160), dpi=300, bbox_inches='tight')
    plt.clf()
    
    return nomfich



#i=0



#data = lire_fichier("../DATA/corpora_SPACY_CONCAT/ADAM/ADAM_krakenbase/ADAM_Mon-village_Kraken-base_txt_md_spacy_cluster.json")
#data = lire_fichier("../DATA/corpora_SPACY_CONCAT/AIMARD_TRAPPEURS/AIMARD-TRAPPEURS_TesseractFra-PNG/AIMARD_les-trappeurs_TesseractFra-PNG_txt_lg_spacy_cluster.json")
path_copora = "../DATA/corpora_SPACY_CONCAT/*/*"

for subcorpus in glob.glob(path_copora):
#    print("SUBCORPUS***",subcorpus)
    
    for path in glob.glob("%s/*spacy_cluster.json"%subcorpus):
        print("PATH*****",path)
        freq = []
        nb_cluster = []
        centro = []
        
       
        nom_fichier = nomfichier(path)
#        print("%s/%s.png"%(subcorpus,nom_fichier))
        data=lire_fichier(path)

        for cle, val in data.items(): 
        #    print(val)
            for att, contenu in val.items():
        #        print(att)
                if att == "Freq. centroide":
        
                    freq.append(contenu)
                    
        #            print(freq)
                if att == "Termes":
                    nb_cluster.append(len(contenu))
        #            print(nb_cluster)
                
                if att == "Centroïde":
                    centro.append(contenu)
        
        liste_1_10=[]
        liste_1_9=[]
        liste_2_10=[]
        liste_2_9 =[]
        y=0
        j=0

        for i in centro:
#            print(freq[y])
            
            if freq[y]== 1 and nb_cluster[j] > 1:
                liste_1_10.append([i,freq[y],nb_cluster[j]])
#                print(liste_1_10)
##        
            if freq[y]== 1 and nb_cluster[j] == 1:
                liste_1_9.append([i,freq[y],nb_cluster[j]])
                
            if freq[y]>= 2 and nb_cluster[j] > 1:
                liste_2_10.append([i,freq[y],nb_cluster[j]])
                
            if freq[y]>= 2 and nb_cluster[j] == 1:
                liste_2_9.append([i,freq[y],nb_cluster[j]])
           
            y=y+1
            j=j+1

        x0=[]
        x1=[]
        x2=[]
        x3=[]
        point_freq1=[]
        point_freq1_9=[]
        point_freq2=[]
        point_freq2_9=[]
        cluster_j0=[]
        cluster_j1=[]
        cluster_j2=[]
        cluster_j3=[]
        
        for m00 in liste_1_10:
        #    print(p)
            x0.append(m00[0])
            point_freq1.append(m00[1]) 
            cluster_j0.append(m00[2])
        plt.scatter(x0,point_freq1, label = "Hapax & cluster > 1",   s=cluster_j0, color= "blue", marker="o")
        
        for m03 in liste_2_10:
        
            x3.append(m03[0])
            point_freq2.append(m03[1]) 
            cluster_j3.append(m03[2])
        plt.scatter(x3,point_freq2, label = "cluster > 1",   s=cluster_j3, color= "red", marker="o")
        
        for m01 in liste_1_9:
        
            x1.append(m01[0])
            point_freq1_9.append(m01[1]) 
            cluster_j1.append(m01[2])
        plt.scatter(x1,point_freq1_9, label = "Hapax & cluster = 1",  s=cluster_j1, color= "cyan", marker="o")
        
        for m02 in liste_2_9:
        
            x2.append(m02[0])
            point_freq2_9.append(m02[1])
            cluster_j2.append(m02[2])
        plt.scatter(x2,point_freq2_9, label = "cluster = 1",  s=cluster_j2, color= "orange", marker="o")
        
        
        
        plt.ylabel("Frequence")
        plt.xlabel("Centroïdes")
        plt.xticks(fontsize=6,rotation=90)
        plt.yticks(fontsize=6)
        plt.axis([-1,len(centro),-1, 115])
        
        
            
        #plt.legend(loc="lower left",ncol=6, bbox_to_anchor=(-0.05,0.98))
        #plt.legend 
        #plt.show()   
        
        stocker_graph("%s/%s.png"%(subcorpus,nom_fichier))   


        
