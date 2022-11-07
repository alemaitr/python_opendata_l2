import requests
from pprint import pprint
import csv

def get_genre(genre, nom_acteur=None):
    url = f"http://my-json-server.typicode.com/alemaitr/python_opendata_l2/cesars2016?genre={genre}"
    donnees = []
    for film in requests.get(url=url).json():
        liste_noms_acteurs = [a.get('nom', '') for a in film["acteurs"]]
        if nom_acteur is None or nom_acteur in liste_noms_acteurs:
            donnees.append(film)
    return donnees


def realisateurs(donnees):
    liste_real = []
    for film in donnees:
        if film["réalisateur"]["prénom"] == "François":
            liste_real.append(film["réalisateur"])
    return liste_real


def get_nom_acteur(acteur):
    return acteur.get("nom", acteur.get("nickname", "")).upper() + " " + acteur.get("prénom", "").upper()


def liste_acteurs_avec_doublons(donnees):
    liste_acteurs = []
    for film in donnees:
        liste_acteurs.extend(film.get("acteurs", []))
    return liste_acteurs


def acteurs_tries(donnees):
    liste_acteurs = liste_acteurs_avec_doublons(donnees)
    liste_acteurs_sans_doublon = []
    for acteur in liste_acteurs:
        if acteur not in liste_acteurs_sans_doublon:
            liste_acteurs_sans_doublon.append(acteur)
    liste_acteurs_tries = sorted(liste_acteurs_sans_doublon, key=get_nom_acteur)
    return liste_acteurs_tries


def acteurs_plusieurs_films(donnees):
    liste_acteurs = liste_acteurs_avec_doublons(donnees)
    liste_acteurs_sans_doublon = []
    liste_acteurs_doublons = []
    for acteur in liste_acteurs:
        if acteur in liste_acteurs_sans_doublon:
            liste_acteurs_doublons.append(acteur)
        else:
            liste_acteurs_sans_doublon.append(acteur)
    return liste_acteurs_doublons


def ajoute_id(donnees):
    for i, film in enumerate(donnees):
        film["id"] = i
    return donnees        


def separe_films_acteurs(donnees):
    liens_films_acteurs = []
    for film in donnees:
        if "acteurs" not in film:
            continue
        for acteur in film["acteurs"]:
            liens_films_acteurs.append({"film": film["id"], "acteur": acteur["id_acteur"]})
        del film["acteurs"]
    return donnees, liens_films_acteurs
    

def linearise_real(donnees):
    for film in donnees:
        for cle, valeur in film["réalisateur"].items():
            film[f"réalisateur.{cle}"] = valeur
        del film["réalisateur"]
    return donnees


# 1. Chargement des données
url = "http://my-json-server.typicode.com/alemaitr/python_opendata_l2/cesars2016"
donnees = requests.get(url=url).json()
pprint(donnees)

# 2. Les Biopic
donnees_biopic = get_genre(genre="Biopic", nom_acteur="de Lencquesaing")
pprint(donnees_biopic)

# 3. Les Réalisateurs
real_Francois = realisateurs(donnees)
print(real_Francois)

# 4. Les acteurs
print(f"Liste des acteurs qui jouent dans plusieurs films : {acteurs_plusieurs_films(donnees)}")

# Pour aller plus loin
# 5. Sauvegarde dans 3 fichiers CSV : acteurs, films, liens acteurs-films
tous_les_acteurs = acteurs_tries(donnees)
print(f"Liste triée des acteurs : {tous_les_acteurs}")
donnees = ajoute_id(donnees)
films, liens_films_acteurs = separe_films_acteurs(donnees, tous_les_acteurs)
pprint(liens_films_acteurs)

fp = open("acteurs.csv", "w")
writer = csv.DictWriter(fp, fieldnames=["id", "prénom", "nom", "nickname"], delimiter=";")
writer.writeheader()
writer.writerows(tous_les_acteurs)
fp.close()

fp = open("liens.csv", "w")
writer = csv.DictWriter(fp, fieldnames=["film", "acteur"], delimiter=";")
writer.writeheader()
writer.writerows(liens_films_acteurs)
fp.close()

donnees = linearise_real(donnees)
fp = open("films.csv", "w")
writer = csv.DictWriter(fp, 
                        fieldnames=['id', 'titre', 'date_sortie', 'durée', 'réalisateur.prénom', 'réalisateur.nom', 'genre'], 
                        delimiter=";")
writer.writeheader()
writer.writerows(donnees)
fp.close()
