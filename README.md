# NER_Cluster

Cet outil est un programme de clustering de données que nous appliqons à des listes d'entité nommées extraites de transcription OCR bruitées.
Ce programme est adapté de : https://stats.stackexchange.com/questions/123060/clustering-a-long-list-of-strings-words-into-similarity-groups

## Dépendances

scikit-learn : https://scikit-learn.org/stable/install.html#installation-instructions

numpy : https://numpy.org/install/

glob :

json : 


## Types d'entrées

Liste d'entités nommées enregistrées dans un fichier.json
Le programme ci-présent est élaboré pour s'éxécuter sur un répertoire, comprenant deux autres niveaux de sous-répertoires avant les fichiers

### Arborescence

Corpus

-Sous-corpus

--OCR

---Ref

----fichier.json

---OCR

----fichier.json

## Sorties

Dictionnaires :
' {

  "ID 0": {
  
    "Centro\u00efde": "amaurdeDieu",
    
    "Freq. centroide": 1,
    
    "Termes": [
    
      "amaurdeDieu"
      
    ]
    
  },
  
  "ID 1": {
  
    "Centro\u00efde": "bSavoyard",
    
    "Freq. centroide": 1,
    
    "Termes": [
    
      "Savoyard",
      
      "bSavoyard"
      
    ]
    
  } ' 
  
### Arborescence

Corpus

-Sous-corpus

--OCR

---Ref

----fichier.json

---OCR

----fichier.json

---fichier_cluster.json

---fichier_non_cluster.json \[liste des fichiers pour lesquels le programme n'a pas pu effectuer le calcul]

