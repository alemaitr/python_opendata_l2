import os
import json
import graphh

def acces_cle_api():
    fp = open("credentials.json", "r", encoding="utf-8")
    data = json.load(fp)
    return data["GraphHopper"]


#Exercice 1

# Question 1
def altitude(lieu1, gh_client):
    latlong_lieu1 = gh_client.address_to_latlong(lieu1)
    
    return gh_client.elevation_point(latlong_lieu1)


# Question 2
def les_altitudes(liste_gps, gh_client):
    alti = []
    for coor in liste_gps:
        lat = coor["lat"]
        lng = coor["lng"]
        alti.append(gh_client.elevation_point((lat, lng)))
    return alti


# Exercice 2
def deniveles(liste_gps, gh_client):
    liste_alti = les_altitudes(liste_gps, gh_client)
    deniv_pos = 0
    deniv_neg = 0

    for i in range(len(liste_alti) - 1):
        delta = liste_alti[i + 1] - liste_alti[i]
        if delta > 0:
            deniv_pos += delta
        else:
            deniv_neg += -delta

    return (deniv_pos, deniv_neg)


# Exercice 3
# Nb : il est nécessaire de convertir le format de coordonnées
def convertit_coords(lst_coords):
    lst2 = []
    for coor in lst_coords:
        lst2.append({"lat": coor["lat"], "lng": coor["lon"]})
    return lst2


def les_randos(fichier, gh_client):
    fp = open(fichier, "r")
    les_randos = json.load(fp)
    for rando in les_randos:
        nom = rando["name"]
        coords = convertit_coords(rando["coords"])
        deniv = deniveles(coords, gh_client)
        print(f"{nom} \n \t - Dénivelé positif cumulé : {deniv[0]:.2f}\n \t - Dénivelé négatif cumulé : {deniv[1]:.2f}")


# Exercice 4
def ecrit_dico(fichier_in, gh_client, fichier_out):
    fp = open(fichier_in, "r")
    les_randos = json.load(fp)
    liste_finale = []
    for rando in les_randos:
        rando_finale = {}
        rando_finale["name"] = rando["name"]
        coords = convertit_coords(rando["coords"])
        deniv = deniveles(coords, gh_client)
        rando_finale["D+"] = round(deniv[0],2)
        rando_finale["D-"] = round(deniv[1],2)
        liste_finale.append(rando_finale)
    fp2 = open(fichier_out, "w")
    json.dump(liste_finale,fp2,indent=2)


#Début des tests
os.chdir("TD5/Corrige")

cle_api = acces_cle_api()
gh_client = graphh.GraphHopper(api_key=cle_api)


#Exercice 1 :altitude
# Test Q1
# print("Altitude de Rennes : ",altitude("Rennes",gh_client))
# print("Altitude de Saint-Malo : ",altitude("Saint-Malo",gh_client))
# print("Altitude de Chamonix : ",altitude("Chamonix",gh_client))
# Altitude de Rennes :  41.08
# Altitude de Saint-Malo :  26.13
# Altitude de Chamonix :  1036.41

# Test Q2
lst_gps = [
    {"lng": -1.426533, "lat": 48.005135},
    {"lng": -1.418127, "lat": 47.986058},
    {"lng": -1.427611, "lat": 47.989871},
    {"lng": -1.430202, "lat": 48.000354}
]
# print(les_altitudes(lst_gps,gh_client))
# [35.29, 64.36, 48.78, 35.81]

# Exercice 2
# print(deniveles(lst_gps,gh_client))
# (29.07, 28.55)

# Exercice 3
# les_randos("../Donnees/mini-rando_gps.json",gh_client)

# Exercice 4
ecrit_dico("../Donnees/mini-rando_gps.json", gh_client, "randos_finales.json")