import csv
import os
import sys
import json
import graphh
import math


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

def plus_court_covoit(origine, dest, options, client):
    duree_min  = math.inf
    option_min = None
    for ville in options:
        temps = duree_lieux(client, origine, ville)+ duree_lieux(client, ville,dest)
        if temps < duree_min :
            duree_min = temps
            option_min = ville
        print(f"En passant par {ville} : {temps} minutes")
    return option_min


#Fonctions pour l'exercice 2
def plus_proche_point(amis, lieux, client):
    dist_min = math.inf
    lieu_min = None
    for ville in lieux :
        somme_trajet = 0
        for qui in amis:
            somme_trajet+=distance_lieux(client, qui, ville)
        if somme_trajet < dist_min:
            dist_min = somme_trajet
            lieu_min = ville
        print(f"A {ville} : distance cumulée {somme_trajet} km")
    return lieu_min


#Fonctions pour l'exercice 3

def plus_proche_partenaire(position, contacts, sport, client):
    dist_min = math.inf
    qui = None
    for partenaire in contacts:
        if partenaire['sport']==sport:
            dist = distance_lieux(client ,position,partenaire['localisation'])
            if dist < dist_min :
                dist_min = dist
                qui = partenaire["nom"]
    return qui


#######################################################################
#Tests et appels de fonctions
#######################################################################
os.chdir("TD2/Corrige")
#Exercice 1
cle_api = acces_cle_api()
gh_client = graphh.GraphHopper(api_key=cle_api)
ville = plus_court_covoit("Rennes","Marseille",["Paris 14ème arrondissement", "Lyon 1er arrondissement", "Bordeaux"],gh_client)
print(f"Il est plus court de passer par {ville}")


#Exercice 2

amis = ["Paris 14ème arrondissement", "Auxerre ", "Lyon 1er arrondissement"]
lieux = ["Rennes", "Strasbourg", "Dijon"]
ville2 = plus_proche_point(amis, lieux, gh_client)
print(f"La ville la plus proche est {ville2}")

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

qui =plus_proche_partenaire("Cesson-Sévigné", liste_dicos, "Tennis", gh_client)
print(f"Le plus proche de Cesson pour jouer au tennis est {qui}")