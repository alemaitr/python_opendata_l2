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
    
#Fonctions pour l'exercice 3

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

#Fonctions pour l'exercice 4

def distances_etapes(voyage, ghclient):
    etapes = []
    for i in range(0,len(voyage)-1):
        dist = distance_lieux(ghclient, voyage[i], voyage[i+1])
        etapes.append(dist)
    return etapes


def distance_totale(voyage, gh_client):
    etapes = distances_etapes(voyage, gh_client)
    return sum(etapes)




#######################################################################
#Tests et appels de fonctions
#######################################################################
os.chdir("TD1/Corrige")

#Exercice 1
macle = acces_cle_api()
print(f"Ma clé d'API : {macle}")

#Exercice 2
gh_client = graphh.GraphHopper(api_key=macle)

coor_beaulieu = gh_client.address_to_latlong("Rennes Beaulieu")
coor_villejean = gh_client.address_to_latlong("Rennes Villejean")

print(f"Coordonnées de Beaulieu {coor_beaulieu}")
print(f"Coordonnées de Villejean {coor_villejean}")

dist_beaulieu_villejean = gh_client.distance([coor_beaulieu,coor_villejean],"km")
print(f"Distance de Beaulieu à Villejean {dist_beaulieu_villejean}km")

dist_villejean_beaulieu = gh_client.distance([coor_villejean,coor_beaulieu],"km")
print(f"Distance de Villejean à Beaulieu {dist_villejean_beaulieu}km")

duree_villejean_beaulieu_voit = gh_client.duration([coor_villejean,coor_beaulieu],unit="min")
print(f"Durée de Villejean à Beaulieu en voiture {duree_villejean_beaulieu_voit}min")

# duree_villejean_beaulieu_velo = gh_client.duration([coor_villejean,coor_beaulieu],vehicle ="bike",unit="min")
# print(f"Durée de Villejean à Beaulieu en vélo {duree_villejean_beaulieu_velo}min")


#Exercice 3
dist = distance_lieux(gh_client,"Rennes", "Brest")
print(f"Distance entre Rennes et Brest {dist} km")
duree = duree_lieux(gh_client,"Rennes", "Brest")
print(f"Durée entre Rennes et Brest {duree} min")


#Exercice 4
voyage1 = ["Rennes","Le Mans", "Tours", "Clermont-Ferrand", "Avignon"]
voyage2 = ["Rennes", "Chateaugiron", "Chateaubourg", "Vitré", "Fougères"]

print(f"Distance des étapes du 1er voyage : {distances_etapes(voyage1,gh_client)}")
print(f"Distance des étapes du 2nd voyage : {distances_etapes(voyage2,gh_client)}")

print(f"Distance totale du 1er voyage : {distance_totale(voyage1,gh_client)}km")
print(f"Distance totale du 2nd voyage : {distance_totale(voyage2,gh_client)}km")