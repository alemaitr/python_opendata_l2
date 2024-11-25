import os
import json
import csv
from pprint import pprint
import requests 
import dico_dpt
import graphh
from cartographie import *

##############################################################
###### Corrigé du projet des L2 de décembre 2024 par Aurélie Lemaitre
##############################################################

## Fonction qui accède à la clé api et renvoie un client graphHopper
def cree_client_graphHopper():
    fp = open("credentials.json", "r", encoding="utf-8")
    data = json.load(fp)
    cle = data["GraphHopper"]
    return graphh.GraphHopper(cle)

## Fonction qui prend en entrée un clien graphh et les coordonnées GPS de deux lieux. 
## Calcule et renvoie la durée du trajet en voiture entre ces deux lieux
def duree_lieux(ghclient, coor1, coor2):
    duree = ghclient.duration([coor1,coor2],unit="min")
    return duree


## Fonction qui prend en entrée le fichier des tresors, le fichier des trouvailles, un type de trésor
## et renvoie la liste des trésors de ce type non encore trouvés par Tic et Tac.
def construit_liste_tresors_candidats(fichier_tresors, fichier_trouvailles, type_tresor):
    les_tresors = charge_tresors_type(fichier_tresors,type_tresor)
    tresors_non_trouves = filtre_tresors_trouves(les_tresors,fichier_trouvailles)
    return tresors_non_trouves

## Fonction qui charge les trésors contenus dans le fichier et renvoie la liste de ceux du type attendu
def charge_tresors_type(fichier,type_tresor):
    lst_tresors = []
    with open(fichier,"r",encoding='utf-8') as fp :
        tous_tresors = json.load(fp)
    for t in tous_tresors :
        if t["type"]==type_tresor:
            lst_tresors.append(t)
    return lst_tresors

## Fonction qui prend un liste de trésors, un fichier contenant les trouvailles
## qui renvoie la liste des trésors non déjà trouvés
def filtre_tresors_trouves(lst_tresors, trouvailles):
    lst_fin = []
    lst_trouves = charge_id_trouvailles(trouvailles)
    for t in lst_tresors :
        if t["nid"] not in lst_trouves:
            lst_fin.append(t)
    return lst_fin

## Fonction qui charge les trouvailles et renvoie la liste des id de tresors déjà trouvés
def charge_id_trouvailles(trouvailles):
    lst_id = []
    with open(trouvailles,"r") as fp:
        for trouve in csv.DictReader(fp,delimiter=";") :
            lst_id.append(trouve["id_tresor"])
    return lst_id
    
## Fcontion qui prend en entrée un opérateur, un nom à exclure, et une liste de départements. 
## Cette fonction renvoie la liste des hotels de cet opérateur dans ces départements
## On représente un hotel par un dictionnaire
def construit_liste_hotels_possibles(nom_operateur,mot_exclure,lst_dpt):
    
    # Récupération de la liste de tous les hotels de l'opérateur
    url = f"https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/osm-hosting-fr@babel/records?limit=100&refine=operator%3A%22{nom_operateur}%22"
    reponse = requests.get(url).json()
    lst_hotels = []

    for hotel in reponse["results"]:
        dpt = int(hotel["code_departement"])       
        if dpt in lst_dpt :
            nom = hotel['name']
            if mot_exclure not in nom :
                dico={}
                dico["nom"]=f"{hotel['name']} à {hotel['commune']}"
                dico["coord"]=hotel["geo_point_2d"]
                lst_hotels.append(dico)

    return lst_hotels

## Fonction qui prend en parametre un fichier de référence des départements, et le nom de la région
## Retourne la liste des departements de la région
def extrait_numeros_departements(region):
    dept = []
    for num,nom in dico_dpt.dpt_region.items():
        if nom == region :
            dept.append(num)
    return dept

## Fonction qui prend en paramètre un client graphh le dico d'un hotel et la liste des tresors, ainsi qu'une duree
## Renvoie la liste des tresors situées à un temps de trajet inférieur à la durée de l'hotel
def tresors_proche_hotel(gh_client, hotel, les_tresors, duree):
    tresor_proche = []
    coord_hotel = (float(hotel["coord"]["lat"]),float(hotel["coord"]["lon"]))
    for tres in les_tresors:
        coord_tres = (float(tres["lat"]),float(tres["lng"]))
        temps = duree_lieux (gh_client,coord_hotel,coord_tres)
        print(f"\t \t {tres['nom']} ({tres['departement']}) est à une durée de {temps} min de {hotel['nom']}")
        if temps < duree :
            tresor_proche.append(tres)
    print(f"Il y a {len(tresor_proche)} trésors proches de {hotel['nom']}")
    return tresor_proche

## Fonction qui prend en entrée les hotels et les trésors candidats, et renvoie le meilleur hotel
## Renvoie un tuple contenant l'hotel, ainsi que les trésors à proximité
def trouve_meilleur_hotel(gh_client,hotels,tresors,duree):
    nb_proche = 0
    best_hotel = None
    tresors_proches = []
    for h in hotels :
        proche = tresors_proche_hotel(gh_client,h,tresors,duree)
        if len(proche)>nb_proche:
            nb_proche = len(proche)
            best_hotel = h
            tresors_proches=proche
    return (best_hotel,tresors_proches)

## Fonction qui écrit le csv des trésors à trouver
def ecrit_csv(fichier,tresors):
    with open(fichier, 'w', newline='',encoding='utf-8') as csvfile:
        fieldnames = tresors[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for t in tresors :
            writer.writerow(t)
    
## Fonction qui crée et affiche la carte des trésors
## Prend en entrée : l'hotel, les tresors proches, les tresors non trouves
def creer_carte_terra_aventura(hotel,proches,non_trouves):
    carte = creer_carte("Trésors de Terra Aventura")
    #Point bleu pour l'hotel
    tracer_point(carte,float(hotel["coord"]["lon"]),float(hotel["coord"]["lat"]),hotel["nom"],"blue")
    
    #Points verts pour les caches accessibles
    for tres in proches :
        tracer_point(carte,float(tres["lng"]),float(tres["lat"]),tres["nom"],"green")

    #Points rouge pour les caches à plus d'une heure de route de l'hotel
    for tres in non_trouves :
        if tres not in proches :
            tracer_point(carte,float(tres["lng"]),float(tres["lat"]),tres["nom"],"red")
    
    afficher_carte(carte)

if __name__=="__main__":
    os.chdir("ProjetTerraAventura")
    # Préparation de la liste des départements de Nouvelle Aquitaine => Utilisation du fichier dico_dpt.py
    departements = extrait_numeros_departements("Nouvelle-Aquitaine")
    print(f"Les numéros de département de région Nouvelle-Aquitaine sont : {departements}")

    # Création du client graphHopper
    gh_client = cree_client_graphHopper()

    # Préparation de la liste des trésors
    tresors = construit_liste_tresors_candidats("tresors.json", "trouvailles.csv", "Zabeth")
    print(f"{len(tresors)} trésors de type Zabeth ont été chargés, non encore trouvés")
    # pprint(tresors)
    print("*"*40)
    
    # Préparation de la liste des hotels
    operateur = "Ibis"
    exclure = "Styles"
    hotels = construit_liste_hotels_possibles(operateur,exclure, departements)
    print(f"{len(hotels)} hotels de type {operateur} ne contenant pas {exclure} sont candidats dans les départements de Nouvelle Aquitaine ")
    # pprint(hotels)
    print("*"*40)
    
    # Recherche du meilleur_hotel
    (hotel,proches) = trouve_meilleur_hotel(gh_client,hotels,tresors,60)
    print("*"*40)
    print(f"Le meilleur hotel est l'hotel {hotel['nom']}")
    print("Il permet d'accéder aux trésors : ")
    for tres in proches :
        print(f"\t {tres['nom']} à {tres['ville']} ({tres['departement']})")
    print("*"*40)
    
    #Ecriture du fichier csv
    ecrit_csv("a_trouver.csv",proches)

    #Création de la carte
    creer_carte_terra_aventura(hotel,proches,tresors)

# Le meilleur hotel est l'hotel Ibis à Bordeaux
# Il permet d'accéder aux trésors :
#     Echappée belle en Pays Gabaye à Saint-Savin (33)
#     Le marathon de l’échasse à Salles (33)
#     Pardaillan, chevalier maudit à Gensac (33)
#     Reine d’un jour... à Coutras (33)