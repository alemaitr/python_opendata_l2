import csv
import json
import os
from pprint import pprint

import requests


#Fonction qui renvoie une liste de prefectures, chaque prefecture sous la forme d'un dictionnaire
def obtient_prefectures():
    with open("v_region_2025.csv",encoding="utf-8") as fp : 
        contenu = csv.DictReader(fp,delimiter=",")
        lst_villes = []
    
        for dico in contenu :
            v = {}
            v["Code"] = dico["CHEFLIEU"]
            v["Region"] = dico["LIBELLE"]
            lst_villes.append(v)
    
    with open("communes_gps.json",encoding="utf-8") as fp :
        contenu = json.load(fp)
        for ville in lst_villes :
            for dico in contenu :
                if dico["CODE_INSEE"] == ville["Code"]:
                    ville["Nom"] = dico["NOM"]
                    ville["Lat"] = dico["LATITUDE"]
                    ville["Long"] = dico["LONGITUDE"]
    return lst_villes

#Fonction qui enrichit les dictionnaires des villes avec la pollution
def obtient_pollution(lst_villes, enligne=False):
    if enligne :
        cle = lit_cle_api()
        for ville in lst_villes :
            lat = ville["Lat"]
            lon = ville["Long"]
            url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={cle}"
            rep = requests.get(url=url).json()
            ville["Pollution"] = rep["list"][0]["components"]["pm2_5"]
    
    else : 
        with open("villes_pollution.json",encoding="utf-8") as fp :
            contenu = json.load(fp)
            for ville in lst_villes :
                for dico in contenu :
                    if dico["CODE_INSEE"] == ville["Code"]:
                        ville["Pollution"] = dico["POLLUTION"]

#Fonction qui enrichit les dictionnaires des villes avec la température
def obtient_temperature(lst_villes, enligne=False):
    if enligne :
        cle = lit_cle_api()
        for ville in lst_villes :
            lat = ville["Lat"]
            lon = ville["Long"]
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={cle}&units=metric"
            rep = requests.get(url=url).json()
            print(rep)
            ville["Temperature"] = rep['main']['temp']
    else : 
        with open("villes_temperature.json",encoding="utf-8") as fp :
            contenu = json.load(fp)
            for ville in lst_villes :
                for dico in contenu :
                    if dico["CODE_INSEE"] == ville["Code"]:
                        ville["Temperature"] = dico["TEMPERATURE"]


#Notation par étoiles de la température
def notation_temperature(lst_ville):
    for ville in lst_ville:
        temp = ville["Temperature"]
        if temp > 19 and temp <21:
            ville["*temp"] = 5
        elif temp > 18 and temp < 22:
            ville["*temp"] = 4
        elif temp > 15 and temp < 25:
            ville["*temp"] = 3
        elif temp > 10 and temp < 30:
            ville["*temp"] = 2
        else :
            ville["*temp"] = 1
    #La liste des villes est automatiquement enrichie (modification en place du dictionnaire)

#Notation par étoiles de la pollution
def notation_pollution(lst_ville):
    for ville in lst_ville:
        poll = ville["Pollution"]
        if poll <=1 :
            ville["*poll"] = 5
        elif poll <=2:
            ville["*poll"] = 4
        elif poll <=5:
            ville["*poll"] = 3
        elif poll <=10:
            ville["*poll"] = 2
        else :
            ville["*poll"] = 1
    #La liste des villes est automatiquement enrichie (modification en place du dictionnaire)

def classement(les_prefectures):
    les_prefectures.sort(key=lambda x: x["*poll"]+x["*temp"],reverse = True)   


def lit_cle_api():
    with open("credentials.json", "r") as f:
        creds = json.load(f)
    return creds["OpenWeather"]


#Extraction et affichage des données
os.chdir("ProjetMeteo")
les_prefectures = obtient_prefectures()
# pprint(les_prefectures)

#Chargement de la météo et de la température
#La liste les_prefectures est automatiquement enrichie (modification en place du dictionnaire)
obtient_temperature(les_prefectures,enligne=True)
obtient_pollution(les_prefectures,enligne=True)
# pprint(les_prefectures)

for ville in les_prefectures:
    print(f"{ville['Nom']} : température {ville['Temperature']}°C - pollution {ville['Pollution']}µg/m3")



# Notation par étoile
notation_temperature(les_prefectures)
notation_pollution(les_prefectures)
# pprint(les_prefectures)
print("Nom de la ville | Note météo  | Note pollution")
for ville in les_prefectures:
    print(f"{ville['Nom']}   \t| {ville['*temp']} \t |{ville['*poll']}") 


# Classement final
classement(les_prefectures)
print("Les meilleures préfectures ")
print("Nom de la ville | Note météo  | Note pollution")
for ville in les_prefectures[:5]:
    print(f"{ville['Nom']}   \t| {ville['*temp']} \t |{ville['*poll']}") 

# Résultats avec les données hors ligne
# Nom de la ville | Note météo  | Note pollution
# AJACCIO         | 4      |4 
# PARIS           | 2      |5
# ORLEANS         | 2      |5
# DIJON           | 2      |5
# ROUEN           | 2      |5

# Nom de la ville | Note météo  | Note pollution
# NANTES          | 5      |5
# RENNES          | 5      |5
# BORDEAUX        | 5      |5
# TOULOUSE        | 5      |5
# LYON    | 4      |5