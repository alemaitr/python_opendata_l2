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
        "sports": ["Tennis","Squash"],
        "localisation": "Place du recteur Henri Le Moal, Rennes, France"
    },
    {
        "nom": "Ernest",
        "sports": ["Football","Course à pied"],
        "localisation": "Place du Parlement de Bretagne, Rennes, France"
    },
    {
        "nom": "Felix",
        "sports": ["Tennis", "Football"],
        "localisation": "182, rue de l'Alma, Rennes, France"
    },
    {
        "nom": "Sarah",
        "sports": ["Football","Squash", "Tennis"],
        "localisation": "88, rue Alphone Guérin, Rennes, France"
    },
    {
        "nom": "Ingrid",
        "sports": ["Course à pied"],
        "localisation": "3, Mail François Mitterrand, Rennes, France"
    }
]