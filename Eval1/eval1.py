import json
import os
import math 
import graphh
import csv

#Q2.1
def type_restos(donnees):
    types = []
    for resto in donnees :
        le_type = resto["type"]
        if le_type not in types : 
            types.append(le_type)
    return types

#Q2.2
def age_moyen(donnees, type):
    somme_age = 0
    nb_rest = 0
    for resto in donnees :
        if resto["type"]==type:
            nb_rest+=1
            somme_age+=resto["proprietaire"]["age"]
    return somme_age/nb_rest

#Q.3

def acces_cle_api():
    fp = open("credentials.json", "r", encoding="utf-8")
    data = json.load(fp)
    return data["GraphHopper"]
    
def resto_plus_proche(adresse, donnees,t):
    dist_min = math.inf
    nom = None
    gh_client = graphh.GraphHopper(api_key=acces_cle_api())
    coor1 = gh_client.address_to_latlong(adresse)
    print(coor1)
    for resto in donnees :
        if resto["type"]==t :
            coor2 = (resto['gps']['latitude'],resto['gps']['longitude'] )
            dist = gh_client.distance([coor1,coor2],"km")
            print(f"{resto['nom']}, distance : ",dist)
            if dist < dist_min :
                dist_min = dist
                nom  = resto["nom"]
    return nom

def extrait_proprio(resto):
    dico={}
    dico["firstname"]=resto["proprietaire"]["prenom"]
    dico["name"]=resto["proprietaire"]["nom"]
    dico["age"]=resto["proprietaire"]["age"]
    dico["shop"]=resto["nom"]
    return dico

def ecrit_annuaire(restos, fichier):
    proprio = [extrait_proprio(r) for r in restos]
    with open(fichier, "w",encoding='utf-8', newline="") as fp : 
        writer = csv.DictWriter(fp, delimiter=";", fieldnames=proprio[0].keys())
        writer.writeheader()
        for r in proprio:
            writer.writerow(r)
    



os.chdir("Eval1")
#Exercice 1
#Q1.1
with open("SanFrancisco_restaurants.json") as fp:
    restos = json.load(fp)
#Q.1.1
print(f"Le nombre de restaurants est {len(restos)}")

#Exercice 2
#Q2.1
les_types = type_restos(restos)
print(f"Les types de restos : {les_types}")

#Q2.2
# print(f"Age moyen des patrons de pizzeria : {age_moyen(restos,'Pizzeria'):.2f} ans")

#Q2.3
for type in les_types :
    print(f"Age moyen des patrons de {type} : {age_moyen(restos,type):.2f} ans")

#Q3.1

print("Le restaurant de ccuisine japonaise le plus proche est ",resto_plus_proche("830 Harrison Street San Francisco", restos,"Cuisine japonaise"))


#Q4.1
ecrit_annuaire(restos,"restaurateurs.csv")