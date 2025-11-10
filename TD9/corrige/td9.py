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
            date = datetime.strptime(dico["date_trouvaille"],"%d/%M/%Y")
            dic_fin[dico["id_tresor"]] = date
    return dic_fin

def enrichit_dico(tresors, trouvaille):
    for t in tresors :
        id = t["nid"]
        if id in trouvaille :
            date = trouvaille[id]
            t["trouvaille"] = date
        else :
            t["trouvaille"] = None

def ecrit_mes_tresors(tresors,fichier):
    lst = []
    for tres in tresors :
        dic = {}
        dic["lat"] = tres["lat"]
        dic["lng"] = tres["lng"]
        dic["trouvaille"] = str(tres["trouvaille"])
        dic["nom"] = tres["nom"]
        dic["type"] = tres["type"]
        lst.append(dic)

    with open(fichier,"w",encoding="utf-8") as fp : 
        json.dump(lst,fp,indent=2)
    print(f"Fichier {fichier}  écrit avec succès.")

def analyse_donnees(tresors):
    resultat = {}
    for tres in tresors : 
        type = tres["type"]
        if type in resultat :
            dico = resultat[type]
        else :
            dico = {"nb":0,"trouvé": 0}
        dico["nb"] = dico["nb"]+1
        if tres["trouvaille"]:
            dico["trouvé"] = dico["trouvé"]+1
        resultat[type]= dico
    return resultat

def affiche_trouvailles_ordonnees (tresors):
    trouves = [t for t in tresors if t["trouvaille"]]
    trouves.sort(key=lambda x: x["trouvaille"])
    print("_____________________________________________")
    print("Liste des trouvailles par ordre de découverte")
    print("_____________________________________________")
    for t in trouves :
        date = t['trouvaille'].strftime("%d/%M/%Y")
        print(f"Le {date} : {t['nom']} à {t['ville']} ")
    print("_____________________________________________")

def cartographier_trouvailles(tresors):
    carte = creer_carte("Terra Aventura")
    for tres in tresors :
        trouvé = tres["trouvaille"]
        if trouvé :
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
print(tresors[0])

trouvailles = charge_trouvailles()
print(len(trouvailles))
print(trouvailles)

enrichit_dico(tresors, trouvailles)
pprint(tresors[0])
pprint(tresors[1])
# ecrit_mes_tresors(tresors,"corrige/mes_tresors.json")

# ## Exercice 2 : Analyse des données
resultat = analyse_donnees(tresors)
pprint(resultat)

trouvailles = affiche_trouvailles_ordonnees(tresors)


# ## Exercice 3 : Cartographie

cartographier_trouvailles(carte,tresors)

   
