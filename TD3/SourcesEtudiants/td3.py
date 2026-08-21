import csv
import os
import sys
import json



#######################################################################
#Définition des fonctions
#######################################################################
def acces_cle_api():
    fp = open("credentials.json", "r", encoding="utf-8")
    data = json.load(fp)
    return data["OpenRouteService"]
    
#Fonctions pour l'exercice 3


#Fonctions pour l'exercice 4






#######################################################################
#Tests et appels de fonctions
#######################################################################

#Exercice 1

#Exercice 2


#Exercice 3


#Exercice 4
voyage1 = ["Rennes","Le Mans", "Tours", "Clermont-Ferrand", "Avignon"]

