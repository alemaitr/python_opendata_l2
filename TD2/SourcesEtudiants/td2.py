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
    
def distance_lieux(ghclient, lieu1, lieu2):
    coor1 = ghclient.address_to_latlong(lieu1)
    coor2 = ghclient.address_to_latlong(lieu2)
    dist = ghclient.distance([coor1,coor2],"km")
    return dist

def duree_lieux(ghclient, lieu1, lieu2):
    coor1 = ghclient.address_to_latlong(lieu1)
    coor2 = ghclient.address_to_latlong(lieu2)
    duree = ghclient.duration([coor1,coor2],unit="min")
    return duree

#Fonctions pour l'exercice 1


#Fonctions pour l'exercice 2

#Fonctions pour l'exercice 3




#######################################################################
#Tests et appels de fonctions
#######################################################################

#Exercice 1


#Exercice 2


#Exercice 3

liste_dicos = [
    {
        "nom": "Pauline",
        "sport": "Tennis",
        "localisation": "Place du recteur Henri Le Moal, Rennes, France"
    },
    {
        "nom": "Ernest",
        "sport": "Football",
        "localisation": "Place du Parlement de Bretagne, Rennes, France"
    },
    {
        "nom": "Felix",
        "sport": "Tennis",
        "localisation": "Rue Lebastard, Rennes, France"
    },
    {
        "nom": "Sarah",
        "sport": "Football",
        "localisation": "Place du Parlement de Bretagne, Rennes, France"
    },
    {
        "nom": "Ingrid",
        "sport": "Course à pied",
        "localisation": "Mail François Mitterrand, Rennes, France"
    }
]