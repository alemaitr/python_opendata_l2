import json
import datetime as dt
import os
import csv
from pprint import pprint


def tous_les_quartiers(donnees):
    quartiers = []
    for resto in donnees:
        if resto["borough"] not in quartiers:
            quartiers.append(resto["borough"])
    return quartiers


def affiche_restos_Manhattan(donnees):
    for r in donnees:
        if r["borough"] == "Manhattan":
            adresse = f"{r['address']['building']}, {r['address']['street']}, {r['address']['zipcode']} New York, USA"
            print(f"{r['name']}: {adresse}")
            

def encode_date(donnees):    
    for resto in donnees:
        for eval in resto["grades"]:
            eval["date"] = dt.datetime.fromisoformat(eval["date"])
    return donnees


def simplifie_grades(donnees):
    for resto in donnees:
        resto["n_grades"] = len(resto["grades"])
        del resto["grades"]
    return donnees


def recode_gps(donnees):
    for resto in donnees:
        lon, lat = resto["address"]["loc"]["coordinates"]
        del resto["address"]
        resto["latitude"] = lat
        resto["longitude"] = lon
    return donnees

# Exercice 2 : Extraction d'informations élémentaires
# Q1.
nom_fichier = "TD4/NYfood.json"
fp = open(nom_fichier, "r")
restos = json.load(fp)

# Q2.
print(f"Nombre de restos: {len(restos)}")

# Q3.
restos_Manhattan = [r for r in restos if r["borough"] == "Manhattan"]
print(f"Nombre de restos à Manhattan: {len(restos_Manhattan)}")

# Q4.
liste_quartiers = tous_les_quartiers(restos)
print(f"Quartiers: {liste_quartiers}")

# Q5.
affiche_restos_Manhattan(restos)

# Q6.
n = 0
for r in restos:
    n += len(r["grades"])
print(f"Nombre total de notes: {n}")

# Q7.
notes = []
for r in restos:
    for g in r["grades"]:
        if g["grade"] not in notes:
            notes.append(g["grade"])
print(f"Notes existantes : {notes}")

# Exercice 3 : Travail spécifique sur les dates
# Q1.
print(f'Interprétation des dates : {restos[0]["grades"][0]["date"]}"')
print(f'de type {type(restos[0]["grades"][0]["date"])}')

# Q2.
restos = encode_date(restos)
print(f'Interprétation des dates : {restos[0]["grades"][0]["date"]}"')
print(f'de type {type(restos[0]["grades"][0]["date"])}')


# Q3.
# for m in range(1, 13):
#     n = 0
#     for r in restos:
#         for g in r["grades"]:
#             if g["date"].year == 2014 and g["date"].month == m:
#                 n += 1 
#     print(f"{m}/2014: {n} notes")

dico_mois = {i:0 for i in range(1,13)}
for r in restos :
    for eval in r["grades"]:
        if eval["date"].year == 2014 :
            dico_mois[eval["date"].month] +=1

for mois, note in enumerate(dico_mois):
    print(f"{mois}/2014: {note} notes")



# Exercice 4 : Export au format CSV
# Q1.
restos = simplifie_grades(restos)
pprint(restos[0])

# Q2.
restos = recode_gps(restos)
pprint(restos[0])

# Q3.
nom_fichier = "NYfood.csv"
fp = open(nom_fichier, "w",encoding='utf-8', newline="")
writer = csv.DictWriter(fp, delimiter=";", fieldnames=restos[0].keys())
writer.writeheader()
for r in restos:
    writer.writerow(r)
fp.close()
