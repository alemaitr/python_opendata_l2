import requests
import csv


    
#Fonction exercice 2

def lesfrancois(content):
    lst =  []
    for film in contenu :
        realisateur = film["réalisateur"]
        if realisateur["prénom"]=="François":
            lst.append(realisateur)
    return lst 

#Fonction exercice 3
def genre_nom(genre,nom_famille=None):
    #On filtre sur le genre
    lst = requests.get(f"http://my-json-server.typicode.com/alemaitr/python_opendata_l2/cesars2016?genre={genre}").json()
    films=[]
    for film in lst :
        acteurs = [a.get("nom","") for a in film["acteurs"]]
        if nom_famille in acteurs or nom_famille==None:
            films.append(film["titre"])
    return films

#Fonction exercice 4
def acteurs_doublons(contenu):
    acteurs = []
    for film in contenu : 
        acteurs.extend(film.get("acteurs",[]))
    return acteurs

def nom_surnom(acteur):
    if "nom" in acteur.keys():
        return acteur["nom"].upper()
    return acteur["surnom"].upper()

def liste_acteur_sans_doublon(contenu):
    liste_db = acteurs_doublons(contenu)
    liste_sans_db = []
    for act in liste_db:
        if act not in liste_sans_db:
            liste_sans_db.append(act)
    liste_sans_db.sort(key=nom_surnom)
    return liste_sans_db

# Note : cette version réutilise 2 fonctions, mais n'est pas la plus économique en 
# terme de nombre de parcours 
def acteurs_plusieurs_films(contenu):
    lst_complete = acteurs_doublons(contenu)
    lst_sans_doublons = liste_acteur_sans_doublon(contenu)
    lst_finale = []
    for acteur in lst_complete :
        if acteur in lst_sans_doublons:
            lst_sans_doublons.remove(acteur)
        else : 
            if acteur not in lst_finale :
                lst_finale.append(acteur)
    return lst_finale

#Fonctions de l'exercice 5

def ajoute_ids(contenu): 
    for i,film in enumerate(contenu) : 
        film["id"]=i
    return contenu

def separe_films_acteurs(contenu):
    liens_acteurs =[]

    for film in contenu :
        id_film = film["id"]
        if "acteurs" in film.keys() :
            for acteur in film["acteurs"] :
                liens_acteurs.append({"id_film":id_film,"id_acteur":acteur["id_acteur"]})
            del film["acteurs"]

    return contenu, liens_acteurs

def prepare_real(contenu):
    for film in contenu :
        film["réalisateur.prénom"] = film["réalisateur"]["prénom"]
        film["réalisateur.nom"] = film["réalisateur"]["nom"]
        del film["réalisateur"]
    return contenu
#Exercice 1
contenu = requests.get("http://my-json-server.typicode.com/alemaitr/python_opendata_l2/cesars2016").json()
print(f"Nombre de films : {len(contenu)}")
# Nombre de films : 8

#Exercice 2
print(lesfrancois(contenu))
# [{'nom': 'Ozon', 'prénom': 'François'}, {'nom': 'Ruffin', 'prénom': 'François'}]

#Exercice 3
print(genre_nom("Biopic","de Lencquesaing"))
# ['La danseuse', 'Chocolat']
print(genre_nom("Biopic"))
# ['La danseuse', 'Chocolat', "L'Odyssée"]

#Exercice 4
acteurs_db = acteurs_doublons(contenu)
# print(acteurs_db)
print(nom_surnom(acteurs_db[0]))
acteurs_diff = liste_acteur_sans_doublon(contenu)
print("La liste des acteurs triée : \n",acteurs_diff)

acteurs_plus = acteurs_plusieurs_films(contenu)

print(f"Nombre d'acteurs dans des films : {len(acteurs_db)}")
print(f"Nombre d'acteurs sans doublons : {len(acteurs_diff)}")
print(f"Nombre d'acteurs dans plusieurs films : {len(acteurs_plus)} : \n {acteurs_plus}")

#Exercice 5
contenu = ajoute_ids(contenu)
print("Après ajout d'id : \n",contenu[0])

#Ecriture des acteurs dans un fichier
acteurs = liste_acteur_sans_doublon(contenu)

with open("acteurs.csv", "w",encoding="utf-8",newline='') as fp :
    writer = csv.DictWriter(fp, fieldnames=["id_acteur", "prénom", "nom", "surnom"], delimiter=";")
    writer.writeheader()
    writer.writerows(acteurs)

#Séparation film/acteurs
contenu, liens = separe_films_acteurs(contenu)

#preparation du réalisateur
contenu = prepare_real(contenu)

#ecriture des films
with open("films.csv", "w",encoding="utf-8",newline='') as fp :
    writer = csv.DictWriter(fp, fieldnames=["id", "titre", "date_sortie", "durée","réalisateur.prénom","réalisateur.nom","genre"], delimiter=";")
    writer.writeheader()
    writer.writerows(contenu)

#ecriture des liens
with open("liens.csv", "w",encoding="utf-8",newline='') as fp :
    writer = csv.DictWriter(fp, fieldnames=["id_film","id_acteur"], delimiter=";")
    writer.writeheader()
    writer.writerows(liens)
