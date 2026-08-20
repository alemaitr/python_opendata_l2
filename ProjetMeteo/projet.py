import csv
import json
import requests

import pprint
import os

def gps_cheflieu(fname_gps, fname_regions):
    gps_data = json.load(open(fname_gps, "r"))

    codes_insee_cheflieu = []
    with open(fname_regions, "r") as fp:
        for dept in csv.DictReader(fp, delimiter=","):
            codes_insee_cheflieu.append(dept["CHEFLIEU"])

    return [ville 
            for ville in gps_data 
            if ville["CODE_INSEE"] in codes_insee_cheflieu]

# def autres_villes(fname_gps, fname_regions):
#     gps_data = json.load(open(fname_gps, "r"))

#     codes_insee_cheflieu = []
#     with open(fname_regions, "r") as fp:
#         for dept in csv.DictReader(fp, delimiter=","):
#             codes_insee_cheflieu.append(dept["CHEFLIEU"])

#     return [ville 
#             for ville in gps_data 
#             if ville["CODE_INSEE"] not in codes_insee_cheflieu]

def read_api_key(api_name):
    with open("credentials.json", "r") as f:
        creds = json.load(f)
    return creds.get(api_name)

def add_temp_pollution(ville):
    lat, lon = ville["LATITUDE"], ville["LONGITUDE"]
    api_key = read_api_key("OpenWeather")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    temp = requests.get(url).json()["main"]["temp"]
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    pollution = requests.get(url).json()["list"][0]["components"]["pm2_5"]
    ville["TEMPERATURE"] = temp
    ville["POLLUTION"] = pollution
    return ville

def ajout_etoiles(ville):
    temp = ville.get("TEMPERATURE")
    pollution = ville.get("POLLUTION")

    # ETOILES_TEMPERATURE
    if 19 <= temp <= 21:
        ville["ETOILES_TEMPERATURE"] = 5
    elif 18 <= temp <= 22:
        ville["ETOILES_TEMPERATURE"] = 4
    elif 15 <= temp <= 25:
        ville["ETOILES_TEMPERATURE"] = 3
    elif 10 <= temp <= 30:
        ville["ETOILES_TEMPERATURE"] = 2
    else:
        ville["ETOILES_TEMPERATURE"] = 1

    # ETOILES_POLLUTION
    if pollution <= 10:
        ville["ETOILES_POLLUTION"] = 5
    elif pollution <= 25:
        ville["ETOILES_POLLUTION"] = 4
    elif pollution <= 50:
        ville["ETOILES_POLLUTION"] = 3
    elif pollution <= 75:
        ville["ETOILES_POLLUTION"] = 2
    else:
        ville["ETOILES_POLLUTION"] = 1

    return ville


fname_gps = os.path.join("data", "communes_gps.json")
fname_cheflieu = os.path.join("data", "v_region_2025.csv")
join_data = gps_cheflieu(fname_gps, fname_cheflieu)
villes_enrichies = [add_temp_pollution(v) for v in join_data]
villes_etoiles = [ajout_etoiles(v) for v in villes_enrichies]

pprint.pprint(
    sorted(
        villes_etoiles,
        key = lambda v: v["ETOILES_POLLUTION"] + v["ETOILES_TEMPERATURE"],
        reverse=True
    )[:3]
)

# les_autres_villes = autres_villes(fname_gps, fname_cheflieu)
# villes_temperature = [
#     {
#         "CODE_INSEE": v["CODE_INSEE"],
#         "TEMPERATURE": v["TEMPERATURE"],
#     }
#     for v in villes_enrichies
# ] + [
#     {
#         "CODE_INSEE": v["CODE_INSEE"],
#         "TEMPERATURE": 12.,
#     }
#     for v in les_autres_villes
# ]

# villes_pollution = [
#     {
#         "CODE_INSEE": v["CODE_INSEE"],
#         "POLLUTION": v["POLLUTION"],
#     }
#     for v in villes_enrichies
# ] + [
#     {
#         "CODE_INSEE": v["CODE_INSEE"],
#         "POLLUTION": 12.5,
#     }
#     for v in les_autres_villes
# ]

# json.dump(villes_temperature, open("data/villes_temperature.json", "w"), indent=2)
# json.dump(villes_pollution, open("data/villes_pollution.json", "w"), indent=2)
