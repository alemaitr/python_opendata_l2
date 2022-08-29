import csv
import os
import sys
import json
import graphh


#######################################################################
#Définition des fonctions
#######################################################################
def acces_cle_api():
    fp = open("credentials.json", "r", encoding="utf-8")
    data = json.load(fp)
    return data["GraphHopper"]
    
#Fonctions pour l'exercice 4

#Fonctions pour l'exercice 5






#######################################################################
#Tests et appels de fonctions
#######################################################################
os.chdir("TD2")

#Exercice 1

#Exercice 2


#Exercice 3


#Exercice 4


#Exercice 5
