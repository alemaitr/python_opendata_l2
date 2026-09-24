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

def distance_trajet_adresse(cle, adresse1, adresse2):
    coord1 = adresse_vers_gps(cle, adresse1)
    coord2 = adresse_vers_gps(cle, adresse2)
    return distance_trajet_coord(cle, coord1, coord2)

def duree_trajet_coord(cle, coord_lieu1, coord_lieu2, mode="driving-car"):
    url = f"https://api.openrouteservice.org/v2/directions/{mode}"
    dico_params={"api_key": cle, "start": coord_lieu1, "end":coord_lieu2}
    reponse = requests.get(url,params=dico_params)
    donnees = reponse.json()
    duree = donnees["features"][0]["properties"]["summary"]["duration"] /60 #La durée est renvoyée en minutes
    return duree

def duree_trajet_adresse(cle, adresse1, adresse2):
    coord1 = adresse_vers_gps(cle, adresse1)
    coord2 = adresse_vers_gps(cle, adresse2)
    return duree_trajet_coord(cle, coord1, coord2)

def distances_etapes(cle, voyage):
    
    # Calcul des coordonnées de tout le voyage
    # C'est moint couteux de le faire une seule fois pour chaque étape avant.
    coord_voyage = []
    for lieu in voyage :
        coord_voyage.append(adresse_vers_gps(cle,lieu))
    # print("Coordonnées du voyage : ",coord_voyage)

    etapes = []
    for i in range(0,len(coord_voyage)-1):
        dist = distance_trajet_coord(cle, coord_voyage[i], coord_voyage[i+1])
        etapes.append(dist)
    return etapes


def distance_totale(cle, voyage):
    etapes = distances_etapes(cle, voyage)
    return sum(etapes)




#######################################################################
#Tests et appels de fonctions
#######################################################################
os.chdir("TD3/Corrige")


#-----------------------------------------------------------
#Exercice 1
#-----------------------------------------------------------

#Exercice 1
macle = acces_cle_api()
print(f"Ma clé d'API : {macle}")

#Exercice 2

## Test pour Rennes Beaulieu
# adresse = "Rennes Beaulieu"
# reponse = requests.get("https://api.openrouteservice.org/geocode/search", params={"api_key": macle, "text": adresse})
# donnees = reponse.json()
# longitude, latitude = donnees["features"][0]["geometry"]["coordinates"]
# print(f"Latitude : {latitude}, Longitude : {longitude}")

#Test avec la fonction
coor_villejean = adresse_vers_gps(macle,"Villejean Université Rennes")
print("Coordonnées de Villejean",coor_villejean)

coor_beaulieu= adresse_vers_gps(macle,"Campus de Beaulieu Rennes")
print("Coordonnées de Beaulieu",coor_beaulieu)

#Exercice 3

# dist_villejean_beaulieu = distance_trajet_coord(macle,coor_villejean,coor_beaulieu)
# print(f"Distance de Villejean à Beaulieu {dist_villejean_beaulieu}km")

# dist_beaulieu_villejean = distance_trajet_coord(macle, coor_beaulieu,coor_villejean)
# print(f"Distance de Beaulieu à Villejean {dist_beaulieu_villejean}km")

# dist_Rennes_Brest = distance_trajet_adresse(macle, "Rennes, France", "Brest, France")
# print(f"Distance de Rennes à Brest {dist_Rennes_Brest}km")


#Exercice 4

# duree_villejean_beaulieu_voit = duree_trajet_coord(macle,coor_villejean,coor_beaulieu)
# print(f"Durée de Villejean à Beaulieu en voiture {duree_villejean_beaulieu_voit}min")

# duree_villejean_beaulieu_velo = duree_trajet_coord(macle,coor_villejean,coor_beaulieu,"cycling-regular")
# print(f"Durée de Villejean à Beaulieu en vélo {duree_villejean_beaulieu_velo}min")

# duree_villejean_beaulieu_pied = duree_trajet_coord(macle,coor_villejean,coor_beaulieu,"foot-walking")
# print(f"Durée de Villejean à Beaulieu à pied {duree_villejean_beaulieu_pied}min")

# duree_rennes_marseille = duree_trajet_adresse(macle, "Rennes, France", "Marseille, France")
# print(f"Durée de Rennes à Marseille en voiture : {duree_rennes_marseille} minutes soit {duree_rennes_marseille//60} heures et {duree_rennes_marseille%60} minutes.")


#Exercice 5
# voyage1 = ["Rennes","Le Mans", "Tours", "Clermont-Ferrand", "Avignon"]
# voyage2 = ["Rennes", "Chateaugiron", "Chateaubourg", "Vitré", "Fougères"]

# print(f"Distance des étapes du 1er voyage : {distances_etapes(macle, voyage1)}")
# print(f"Distance des étapes du 2nd voyage : {distances_etapes(macle, voyage2)}")

# print(f"Distance totale du 1er voyage : {distance_totale(macle,voyage1)}km")
# print(f"Distance totale du 2nd voyage : {distance_totale(macle,voyage2)}km")

# Distance des étapes du 1er voyage : [154.86, 97.3817, 336.3595, 386.72740000000005]
# Distance totale du 1er voyage : 975.3286km

# Distance des étapes du 2nd voyage : [15.9442, 10.9711, 19.0518, 30.902900000000002]
# Distance totale du 2nd voyage : 76.87km
