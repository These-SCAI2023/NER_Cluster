import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.neighbors import DistanceMetric
from sklearn.feature_extraction.text import CountVectorizer
import distance
import sklearn
import json
import glob
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
#
path_copora = "../DATA/corpora_SPACY2.3.5_CLUSTER/DAUDET/DAUDET_kraken-base"
#path_copora = "../DATA/AIMARD_euclidean_damping09/*/*"


for subcorpus in glob.glob(path_copora):
#    print("SUBCORPUS***",subcorpus)
    liste_nom_fichier =[]
    for path in glob.glob("%s/DAUDET_MOD/*lg_spacy.json-concat.json"%subcorpus):
#        print("PATH*****",path)
        
        nom_fichier = nomfichier(path)
#        print(nom_fichier)
        liste=lire_fichier(path)
        
#### FREQUENCE ########
        
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
        freq=len(dic_mots.keys())
        
        
#### VECTORISATION
        #####SI CORRECTION SUR LA LISTE 
#        texte=",".join(liste)
#        print(texte)
#        sup_chaine=re.sub("Ce |ce |Les |Les |les |Si |si |Sa |sa |Je |je |Eh |Tu |tu |il |Il |L*","",texte)
#        liste_sup_chaine=sup_chaine.split(",")
#        print(liste_sup_chaine)
#        Set_00 = set(liste_sup_chaine)
#        print(Set_00)

        Set_00 = set(liste)
        Liste_00 = list(Set_00)
        dic_output = {}
        liste_words=[]
        matrice=[]
        
        for l in Liste_00:
            if len(l)!=1:
                liste_words.append(l)

        try:
            words = np.asarray(liste_words) #So that indexing with a list will work
            for w in words:
                liste_vecteur=[]
            
                    
                for w2 in words:
                
                        V = CountVectorizer(ngram_range=(2,3), analyzer='char')# Vectorisation bigramme et trigramme de caractères 
#                        dist = DistanceMetric.get_metric("jaccard") #choix de la distance de jaccard
                        X = V.fit_transform([w,w2]).toarray()
#                        distance_tab1=dist.pairwise(X) # calcul pour la distance de jaccard
                        distance_tab1=sklearn.metrics.pairwise.cosine_distances(X) # Distance avec cosinus            
                        liste_vecteur.append(distance_tab1[0][1])# stockage de la mesure de similarité
                    
            #    print(liste_vecteur)
            
            
            #  
                matrice.append(liste_vecteur)
            matrice_def=-1*np.array(matrice)
            #print(matrice)
            
    ##### CLUSTER
            
            ###lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])   
            ###affprop = AffinityPropagation(affinity="precomputed", damping= 0.9, random_state = None)
            #affprop.fit(lev_similarity)        
            affprop = AffinityPropagation(affinity="precomputed", damping= 0.5, random_state = None) 
    
            affprop.fit(matrice_def)
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
            #    print(dic_output)
            stocker("%s/%s_cluster-consinus-2-3-clean.json"%(subcorpus,nom_fichier),dic_output)

        except :        
            print("**********Non OK***********", path)

    
            liste_nom_fichier.append(path)
            stocker("%s/fichier_non_cluster.json"%subcorpus, liste_nom_fichier)
            
            continue 
#   

    
