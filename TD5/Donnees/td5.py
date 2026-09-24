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

    

# Question 2

# Exercice 2

# Exercice 3

# Exercice 4

########################################################################
#Début des tests
########################################################################

# Exercice 1



# Exercice 2

# Exercice 3

# Exercice 4


