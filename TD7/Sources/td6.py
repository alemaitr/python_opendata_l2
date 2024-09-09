import csv
import os
import sys
import json
from cartographie import afficher_carte, creer_carte, tracer_point, tracer_ligne

#######################################################################
#Définition des fonctions
#######################################################################
def taille_max(fichier):
    tmax = 0
    fp = open(fichier, "r", encoding="utf-8")
    for ligne in fp.readlines():
        tmax = max(tmax,len(ligne))
    return tmax

#Fonctions pour l'exercice 2


#Fonctions pour l'exercice 4

#Fonctions pour l'exercice 5






#######################################################################
#Tests et appels de fonctions
#######################################################################

#Exercice 2


#Exercice 3


#Exercice 4


#Exercice 5
