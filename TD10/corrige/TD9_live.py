import requests
import csv
import datetime
from pprint import pprint

def get_etapes(url):
    d_etapes = {}
    contenu_brut = requests.get(url)
    contenu_json = contenu_brut.json()
    etapes = contenu_json["etapes"]
    for e in etapes:
        code_etape = e["code_etape"]
        borne_depart = e["depart"]["borne"]
        borne_arrivee = e["arrivee"]["borne"]
        d_etapes[code_etape] = {
            "borne_depart": borne_depart,
            "borne_arrivee": borne_arrivee
        }
    return d_etapes

def validation_equipes(nom_fichier):
    d_validation = {}
    fp = open(nom_fichier, "r")
    for ligne in csv.DictReader(fp, delimiter=";"):
        equipe_id = ligne["equipe_id"]
        date = datetime.datetime.strptime(ligne["date"], "%d/%m/%Y %H:%M")
        if equipe_id not in d_validation.keys():
            d_validation[equipe_id] = {
                ligne["borne_id"]: date
            }
        else:
            d_validation[equipe_id][ligne["borne_id"]] = date
    return d_validation




pprint(get_etapes("http://my-json-server.typicode.com/alemaitr/python_opendata_l2/rennes2express"))

pprint(validation_equipes("TD9_2024/donnees/validation_badge.csv"))