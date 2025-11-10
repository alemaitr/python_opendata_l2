import csv
import datetime
import requests
import pprint
import json
from graphh import GraphHopper


def validations_equipes(fname_validation_badge):
    pos_equipes = {}
    with open(fname_validation_badge, "r") as fp:
        reader = csv.DictReader(fp, delimiter=";")
        for row in reader:
            if row["equipe_id"] not in pos_equipes.keys():
                pos_equipes[row["equipe_id"]] = {}
            # pos_equipes[row["equipe_id"]][row["borne_id"]] = row["date"]
            pos_equipes[row["equipe_id"]][row["borne_id"]] = datetime.datetime.strptime(row["date"], "%d/%m/%Y %H:%M")
    return pos_equipes

def positions_bornes(fname_bornes):
    dico_bornes = {}
    with open(fname_bornes, "r") as fp:
        reader = csv.DictReader(fp, delimiter=";")
        for row in reader:
            dico_bornes[row["borne_id"]] = [float(row["lat"]), float(row["long"])]
    return dico_bornes

def calcule_distance(pos_depart, pos_arrivee):
    api_key = json.load(open("credentials.json", "r"))["GraphHopper"]
    gh_client = GraphHopper(api_key)
    return gh_client.distance([pos_depart, pos_arrivee], unit="km")

def get_etapes(url):
    etapes = requests.get(url).json()["etapes"]
    etapes_distance = {}
    for e in etapes:
        borne_depart = e["depart"]["borne"]
        borne_arrivee = e["arrivee"]["borne"]
        etapes_distance[e["code_etape"]] = {
            "borne_depart": borne_depart,
            "borne_arrivee": borne_arrivee
        }
    return etapes_distance

def duree_par_etape(pos_equipes, etapes):
    durees = {}
    for code_etape, e in etapes.items():
        borne_depart = e["borne_depart"]
        borne_arrivee = e["borne_arrivee"]
        liste_durees = []
        for equipe_id, equipe_infos in pos_equipes.items():
            duree_etape = equipe_infos[borne_arrivee] - equipe_infos[borne_depart]
            liste_durees.append((equipe_id, duree_etape))
        # durees[code_etape] = liste_durees
        durees[code_etape] = sorted(liste_durees, key=lambda t: t[1])
    return durees

def affiche_classement_par_etape(durees):
    etapes = get_etapes("http://my-json-server.typicode.com/alemaitr/python_opendata_l2/rennes2express")
    bornes = positions_bornes("bornes.csv")
    for code_etape, dur in durees.items():
        borne_depart = etapes[code_etape]["borne_depart"]
        borne_arrivee = etapes[code_etape]["borne_arrivee"]
        dist = calcule_distance(bornes[borne_depart], bornes[borne_arrivee])
        print(f"Classement de l'étape {code_etape} ({dist:.1f} km)")
        for idx_t, t in enumerate(dur):
            print(f"  {idx_t + 1}. Equipe {t[0]} ({int(t[1].total_seconds()) // 60} minutes)")

def get_noms_equipes(url):
    equipes = requests.get(url).json()["equipes"]
    noms_equipes = {}
    for eq_id, infos in equipes.items():
        noms_equipes[eq_id] = infos["nom"]
    return noms_equipes

def duree_totale_par_equipe(durees):
    totaux = {}
    for liste_etape in durees.values():
        for equipe, temps in liste_etape:
            totaux[equipe] = totaux.get(equipe, datetime.timedelta(seconds=0)) + temps
    return totaux

def vainqueurs(durees_totales):
    equipes = get_noms_equipes("http://my-json-server.typicode.com/alemaitr/python_opendata_l2/rennes2express")
    temps_min = max(durees_totales.values())
    equipe_vainqueur_id = None
    for equipe, temps in durees_totales.items():
        if temps <= temps_min:
            equipe_vainqueur_id = equipe
            temps_min = temps
    return equipes[equipe_vainqueur_id]

def affiche_classement_par_points(durees):
    nb_points = {}
    for etape, durees_etape in durees.items():
        for i, points in enumerate([5, 2, 1]):
            equipe_id = durees_etape[i][0]
            nb_points[equipe_id] = nb_points.get(equipe_id, 0) + points
    classement = sorted(nb_points.items(), key=lambda t: t[1], reverse=True)
    print("Classement par points :")
    for i, (equipe, points) in enumerate(classement):
        print(f"  {i + 1}. {equipe} ({points} points)")


equipes = validations_equipes("validation_badge.csv")
etapes = get_etapes("http://my-json-server.typicode.com/alemaitr/python_opendata_l2/rennes2express")
durees = duree_par_etape(equipes, etapes)
print(vainqueurs(duree_totale_par_equipe(durees)))
# affiche_classement_par_etape(durees)
affiche_classement_par_points(durees)
