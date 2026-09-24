import csv
import os
import sys
import json
import requests
import math


#######################################################################
#Définition des fonctions
#######################################################################
def acces_cle_api():
    fp = open("credentials.json", "r", encoding="utf-8")
    data = json.load(fp)
    return data["OpenRouteService"]
    
def adresse_vers_gps(cle, adresse):
    url = "https://api.openrouteservice.org/geocode/search"
    dico_params = {"api_key": cle, "text": adresse}
    reponse = requests.get(url,params=dico_params)
    donnees = reponse.json()
    longitude, latitude = donnees["features"][0]["geometry"]["coordinates"]
    return f"{longitude},{latitude}"

def distance_trajet_coord(cle, coord_lieu1, coord_lieu2):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    dico_params = {"api_key": cle, "start": coord_lieu1, "end":coord_lieu2}
    reponse = requests.get(url,params=dico_params)
    donnees = reponse.json()
    distance = donnees["features"][0]["properties"]["summary"]["distance"]/1000  #La distance est renvoyée en mètres
    return distance


def duree_trajet_coord(cle, coord_lieu1, coord_lieu2, mode="driving-car"):
    url = f"https://api.openrouteservice.org/v2/directions/{mode}"
    dico_params={"api_key": cle, "start": coord_lieu1, "end":coord_lieu2}
    reponse = requests.get(url,params=dico_params)
    donnees = reponse.json()
    duree = donnees["features"][0]["properties"]["summary"]["duration"] /60 #La durée est renvoyée en minutes
    return duree

#Fonctions pour l'exercice 1

def plus_court_covoit(origine, dest, options, cle):
    coord_orig = adresse_vers_gps(cle,origine)
    coord_dest = adresse_vers_gps(cle,dest)
    duree_min  = math.inf
    option_min = None
    for ville in options:
        coord_ville = adresse_vers_gps(cle, ville)
        temps = duree_trajet_coord(cle, coord_orig, coord_ville)+ duree_trajet_coord(cle, coord_ville,coord_dest)
        if temps < duree_min :
            duree_min = temps
            option_min = ville
        print(f"En passant par {ville} : {temps} minutes")
    return option_min


#Fonctions pour l'exercice 2

def plus_proche_point(amis, lieux, cle):
    dist_min = math.inf
    lieu_min = None
    for ville in lieux :
        coord_ville = adresse_vers_gps(cle, ville)
        somme_trajet = 0
        for pos in amis:
            coord_ami = adresse_vers_gps(cle,pos)
            somme_trajet+=distance_trajet_coord(cle, coord_ami, coord_ville)
        if somme_trajet < dist_min:
            dist_min = somme_trajet
            lieu_min = ville
        print(f"A {ville} : distance cumulée {somme_trajet} km")
    return lieu_min

#Fonctions pour l'exercice 3

def plus_proche_partenaire(position, contacts, sport, cle):
    dist_min = math.inf
    qui = None
    coord_position = adresse_vers_gps(cle, position)
    for partenaire in contacts:
        if sport in partenaire['sports'] :
            coord_partenaire = adresse_vers_gps(cle,partenaire['localisation'] )
            dist = distance_trajet_coord(cle ,coord_position,coord_partenaire)
            print(f"Distance avec {partenaire['nom']} : {dist}")
            if dist < dist_min :
                dist_min = dist
                qui = partenaire["nom"]
    return qui



#######################################################################
#Tests et appels de fonctions
#######################################################################
os.chdir("TD4/Corrige")
#Exercice 1

macle = acces_cle_api()

# ville = plus_court_covoit("Rennes","Marseille",["Paris 14ème arrondissement", "Lyon 1er arrondissement", "Bordeaux"],macle)
# print(f"Il est plus court de passer par {ville}")

#Exercice 2


# amis = ["Paris 14ème arrondissement", "Auxerre ", "Lyon 1er arrondissement"]
# lieux = ["Rennes", "Strasbourg", "Dijon"]
# ville2 = plus_proche_point(amis, lieux, macle)
# print(f"La ville la plus proche est {ville2}")

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


lieu = "Place de la République, Rennes, France"
qui =plus_proche_partenaire(lieu, liste_dicos, "Tennis", macle)
print(f"Le plus proche de {lieu} pour jouer au tennis est {qui}")