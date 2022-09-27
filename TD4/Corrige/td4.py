import json
import datetime as dt
import os
import csv
from pprint import pprint


def tous_les_quartiers(donnees):
    quartiers = []
    for r in donnees:
        if r["borough"] not in quartiers:
            quartiers.append(r["borough"])
    return quartiers


def affiche_restos_Manhattan(donnees):
    for r in donnees:
        if r["borough"] == "Manhattan":
            adresse = f"{r['address']['building']}, {r['address']['street']}, {r['address']['zipcode']} New York, USA"
            print(f"{r['name']}: {adresse}")
            

def encode_date(donnees):    
    for r in donnees:
        for g in r["grades"]:
            g["date"] = dt.datetime.fromisoformat(g["date"])
    return donnees


def simplifie_grades(donnees):
    for r in donnees:
        r["n_grades"] = len(r["grades"])
        del r["grades"]
    return donnees


def recode_gps(donnees):
    for r in donnees:
        lon, lat = r["address"]["loc"]["coordinates"]
        del r["address"]
        r["latitude"] = lat
        r["longitude"] = lon
    return donnees

# Extraction d'informations élémentaires
# 1.
nom_fichier = "NYfood.json"
fp = open(nom_fichier, "r")
restos = json.load(fp)

# 2.
print(f"Nombre de restos: {len(restos)}")

# 3.
restos_Manhattan = [r for r in restos if r["borough"] == "Manhattan"]
print(f"Nombre de restos à Manhattan: {len(restos_Manhattan)}")

# 4.
liste_quartiers = tous_les_quartiers(restos)
print(f"Quartiers: {liste_quartiers}")

# 5.
affiche_restos_Manhattan(restos)

# 6.
n = 0
for r in restos:
    n += len(r["grades"])
print(f"Nombre total de notes: {n}")

# 7.
notes = []
for r in restos:
    for g in r["grades"]:
        if g["grade"] not in notes:
            notes.append(g["grade"])
print(f"Notes existantes : {notes}")

# Travail spécifique sur les dates
# 1.
print(restos[0]["grades"][0]["date"])

# 2.
restos = encode_date(restos)
pprint(restos[0])

# 3.
for m in range(1, 13):
    n = 0
    for r in restos:
        for g in r["grades"]:
            if g["date"].year == 2014 and g["date"].month == m:
                n += 1
    print(f"{m}/2014: {n} notes")

# Export au format CSV
# 1.
restos = simplifie_grades(restos)
pprint(restos[0])

# 2.
restos = recode_gps(restos)
pprint(restos[0])

# 3.
nom_fichier = "NYfood.csv"
fp = open(nom_fichier, "w")
writer = csv.DictWriter(fp, delimiter=";", fieldnames=restos[0].keys())
writer.writeheader()
for r in restos:
    writer.writerow(r)
fp.close()
