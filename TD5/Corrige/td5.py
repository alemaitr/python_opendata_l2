import os
import json
import requests

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

#Exercice 1
# Question 1

def altitude_coor(cle, coord):
    url = "https://api.openrouteservice.org/elevation/point"
    dico_params = {"api_key": cle, "geometry": coord}
    reponse = requests.get(url,params=dico_params)
    donnees = reponse.json()
    return donnees["geometry"]["coordinates"][2]

def altitude_adresse(cle, adresse):
    coord = adresse_vers_gps(cle, adresse)
    return altitude_coor(cle, coord)
    

# Question 2
def altitudes_lst_coords(cle,liste_gps):
    alti = []
    for coor in liste_gps:
        coor = f"{coor["lng"]},{coor["lat"]}"
        alti.append(altitude_coor(cle,coor))
    return alti

# # Exercice 2
def deniveles(liste_gps, cle):
    liste_alti = altitudes_lst_coords(cle, liste_gps)
    deniv_pos = 0
    deniv_neg = 0
    for i in range(len(liste_alti) - 1):
        delta = liste_alti[i + 1] - liste_alti[i]
        if delta > 0:
            deniv_pos += delta
        else:
            deniv_neg += -delta
    return (deniv_pos, deniv_neg)

# # Exercice 3

def les_randos(fichier, cle):
    fp = open(fichier, "r")
    les_randos = json.load(fp)
    for rando in les_randos:
        nom = rando["name"]
        coords = rando["coords"]
        deniv = deniveles(coords, cle)
        print(f"{nom} \n \t - Dénivelé positif cumulé : {deniv[0]}\n \t - Dénivelé négatif cumulé : {deniv[1]}")

# Exercice 4
def ecrit_dico(fichier_in, cle, fichier_out):
    with open(fichier_in, "r") as fp : 
        les_randos = json.load(fp)
    liste_finale = []
    for rando in les_randos:
        rando_finale = {}
        rando_finale["name"] = rando["name"]
        coords = rando["coords"]
        deniv = deniveles(coords, cle)
        rando_finale["D+"] = deniv[0]
        rando_finale["D-"] = deniv[1]
        liste_finale.append(rando_finale)
    
    with open(fichier_out, "w") as fp2:
        json.dump(liste_finale,fp2,indent=2)

########################################################################
#Début des tests
########################################################################
os.chdir("TD5/Corrige")

cle_api = acces_cle_api()


#Exercice 1
# Test Q1
# print("Altitude de Rennes : ",altitude_adresse(cle_api, "Rennes, France"))
# print("Altitude de Saint-Malo : ",altitude_adresse(cle_api, "Saint-Malo"))
# print("Altitude de Chamonix : ",altitude_adresse(cle_api, "Chamonix"))
# Altitude de Rennes :  29
# Altitude de Saint-Malo :  9
# Altitude de Chamonix :  2208

# Test Q2
lst_gps = [
    {"lng": -1.426533, "lat": 48.005135},
    {"lng": -1.418127, "lat": 47.986058},
    {"lng": -1.427611, "lat": 47.989871},
    {"lng": -1.430202, "lat": 48.000354}
]
# print(altitudes_lst_coords(cle_api, lst_gps))
# [36, 68, 49, 35]

# Exercice 2
# print(deniveles(lst_gps,cle_api))
# (32, 33)

# Exercice 3
# les_randos("../Donnees/mini-rando_gps.json",cle_api)

# Exercice 4
ecrit_dico("../Donnees/mini-rando_gps.json", cle_api, "randos_finales.json")