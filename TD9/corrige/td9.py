##############################################
# Sujet TD 9 - Terra Aventura
##############################################
# Imports
##############################################
import os
import json
import csv
from datetime import datetime
from pprint import pprint
from cartographie import *

##############################################
# Fonctions 
##############################################

## Exercice 1

def charge_tresors():
    with open("donnees/tresors.json","r",encoding='utf-8') as fp : 
        contenu = json.load(fp)
    return contenu

def charge_trouvailles():
    with open("donnees/trouvailles.csv","r") as fp : 
        contenu = csv.DictReader(fp,delimiter=";")
        dic_fin = {}
        for dico in contenu :
            date = datetime.strptime(dico["date_trouvaille"],"%d/%m/%Y")
            dic_fin[dico["id_tresor"]] = date
    return dic_fin

def enrichit_dico(tresors, trouvaille):
    for t in tresors :
        id = t["nid"]
        if id in trouvaille :
            t["trouvé"] = True
            t["date"] = trouvaille[id]
        else :
            t["trouvé"] = False

## Exercice 2
def analyse_donnees(tresors):
    resultat = {}
    for tres in tresors : 
        type = tres["type"]
        if type in resultat :
            dico = resultat[type]
        else :
            dico = {"nb":0,"trouvé": 0}
        dico["nb"] = dico["nb"]+1
        if tres["trouvé"]:
            dico["trouvé"] = dico["trouvé"]+1
        resultat[type]= dico
    return resultat


def type_prefere(dico_type):
    type_max = None
    trouve_max = -1
    for type, dico_nb in dico_type.items():
        t= dico_nb["trouvé"]
        if t> trouve_max:
            trouve_max = t
            type_max = type
    return type_max

def type_plus_avancé(dico_type):
    type_max = None
    pourc_max = -1
    for type, dico_nb in dico_type.items():
        p= dico_nb["trouvé"]/dico_nb["nb"]
        if p> pourc_max:
            pourc_max = p
            type_max = type
    return type_max

#Exercice 3
def affiche_trouvailles_ordonnees (tresors):
    trouves = [t for t in tresors if t["trouvé"]]
    trouves.sort(key=lambda x: x["date"])
    print("_____________________________________________")
    print("Liste des trouvailles par ordre de découverte")
    print("_____________________________________________")
    for t in trouves :
        date = t['date'].strftime("%d/%m/%Y")
        print(f"Le {date} à {t['ville']} : {t['nom']} ")
    print("_____________________________________________")

def analyse_mois_trouvaille(trouvailles):
    dico_mois = {m:0 for m in range(1,13)}
    for date in trouvailles.values():
        m = date.month
        dico_mois[m]+=1
    return dico_mois




#Exercice 4
def cartographier_trouvailles(tresors):
    carte = creer_carte("Terra Aventura")
    for tres in tresors :
        if tres["trouvé"] :
            couleur = 'blue'
        else : 
            couleur = 'red'
        tracer_point(carte,float(tres["lng"]),float(tres["lat"]),tres["nom"],couleur)
    afficher_carte(carte)

##############################################
# Tests
##############################################
os.chdir("TD9")

## Exercice 1 : Prise en compte des trouvailles

tresors = charge_tresors()
print(len(tresors))
# print(tresors[0])

trouvailles = charge_trouvailles()
print(len(trouvailles))
pprint(trouvailles)

enrichit_dico(tresors, trouvailles)
pprint(tresors[0])
pprint(tresors[1])


## Exercice 2 : Trésor de prédilection
resultat = analyse_donnees(tresors)
pprint(resultat)

print(f"Le type de trésors favori de Marco et Polo est {type_prefere(resultat)}")
# Le type de trésors favori de Marco et Polo est Zabeth
print(f"Le type de trésors sont les trouvailles sont les plus avancées est {type_plus_avancé(resultat)}")
# Le type de trésors sont les trouvailles sont les plus avancées est Ziraider


## Exercice 3 : Ordre des découvertes
affiche_trouvailles_ordonnees(tresors)
mois = analyse_mois_trouvaille(trouvailles)
print(mois)

## Exercice 4 : Cartographie

cartographier_trouvailles(tresors)

   
