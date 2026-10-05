import csv
import os
import sys
import json
import requests


#######################################################################
#Définition des fonctions
#######################################################################
def acces_cle_api():
    fp = open("credentials.json", "r", encoding="utf-8")
    data = json.load(fp)
    return data["OpenRouteService"]
    
def adresse_vers_gps(cle, adresse):
    url = "https://api.heigit.org/pelias/v1/search"
    dico_params = {"api_key": cle, "text": adresse}
    reponse = requests.get(url,params=dico_params)
    donnees = reponse.json()
    longitude, latitude = donnees["features"][0]["geometry"]["coordinates"]
    return f"{longitude},{latitude}"

def distance_trajet_coord(cle, coord_lieu1, coord_lieu2):
    url = "https://api.heigit.org/openrouteservice/v2/directions/driving-car"
    dico_params = {"api_key": cle, "start": coord_lieu1, "end":coord_lieu2}
    reponse = requests.get(url,params=dico_params)
    donnees = reponse.json()
    distance = donnees["features"][0]["properties"]["summary"]["distance"]/1000  #La distance est renvoyée en mètres
    return distance


def duree_trajet_coord(cle, coord_lieu1, coord_lieu2, mode="driving-car"):
    url = f"https://api.heigit.org/openrouteservice/v2/directions/{mode}"
    dico_params={"api_key": cle, "start": coord_lieu1, "end":coord_lieu2}
    reponse = requests.get(url,params=dico_params)
    donnees = reponse.json()
    duree = donnees["features"][0]["properties"]["summary"]["duration"] /60 #La durée est renvoyée en minutes
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
        "localisation": "7, rue Barthélémy Pocquet, Rennes, France"
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
        "localisation": "23, av. Janvier, Rennes"
    },
    {
        "nom": "Ingrid",
        "sports": ["Course à pied"],
        "localisation": "3, Mail François Mitterrand, Rennes, France"
    }
]