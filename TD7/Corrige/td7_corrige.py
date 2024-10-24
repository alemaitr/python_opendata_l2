import csv
import os
import sys
import json
from cartographie import afficher_carte, creer_carte, tracer_point, tracer_ligne

#######################################################################
#Définition des fonctions
#######################################################################
def taille_max(fichier):
    tmax = 0
    fp = open(fichier, "r", encoding="utf-8")
    for ligne in fp.readlines():
        tmax = max(tmax,len(ligne))
    return tmax

#Fonctions pour l'exercice 2
def elimine_sans_coordonnees(liste_trajets):
    nv_lst = []
    for trajet in liste_trajets:
        if trajet["geo_point_2d"]!="":
            nv_lst.append(trajet)
    return nv_lst

def liste_couleurs(liste_trajets):
    lst_color = []
    for trajet in liste_trajets:
        lst_color.append(trajet['Color'])
    return lst_color

def corrige_couleurs(liste_trajets):
    for trajet in liste_trajets:
        if len(trajet['Color']) == 6:
            trajet['Color'] ="#"+trajet['Color']
    return liste_trajets 

#Fonctions pour l'exercice 4
def ajoute_point_trajet(carte, trajet):
    coords = trajet['geo_point_2d'].split(",")
    x = float(coords[1])
    y = float(coords[0])
    nom = trajet['Long Name']
    couleur = trajet["Color"]        
    tracer_point(carte,x,y,nom,couleur)

def carte_tous_points_2d(lst_trajets):
    carte = creer_carte("Points 2D")
    for trajet in lst_trajets:
        ajoute_point_trajet(carte,trajet)
    afficher_carte(carte)

#Fonctions pour l'exercice 5

def prepare_lst_coord(trajet):
    coords = json.loads(trajet['Shape'])['coordinates'][0]
    lst_long = []
    lst_lat = []
    for coord in coords:
        lst_long.append(coord[0])
        lst_lat.append(coord[1])
    trajet["lst_long"]=lst_long
    trajet["lst_lat"]=lst_lat
    return trajet
    
def ajoute_ligne_trajet(carte,trajet):
    lst_lat = trajet['lst_lat']
    lst_long = trajet['lst_long']
    nom = trajet['Long Name']
    couleur = trajet["Color"]        
    tracer_ligne(carte,lst_long,lst_lat,nom,couleur)

def carte_toutes_lignes(lst_trajets):
    carte = creer_carte("Lignes")
    for trajet in lst_trajets:
         ajoute_ligne_trajet(carte,trajet)
    afficher_carte(carte)





#######################################################################
#Tests et appels de fonctions
#######################################################################

#Exercice 2
os.chdir("TD7/Corrige/")
nom_fichier = "mobibreizh-lignes.csv"
print(f"La taille maximale du fichier est {taille_max(nom_fichier)}")

csv.field_size_limit(4000000)
fp = open(nom_fichier, "r", encoding="utf-8")
trajets = []
for ligne in csv.DictReader(fp, delimiter=";"):
    trajets.append(ligne)
    
print(f"Nb de trajets : {len(trajets)}")
print(f"Intitulés des champs disponibles : {trajets[0].keys()}")

trajets = elimine_sans_coordonnees(trajets)
print(f"Nb de trajets après supression des trajets sans coordonnees: {len(trajets)}")

# print(f"Les couleurs avant traitement {liste_couleurs(trajets)}")
trajets = corrige_couleurs(trajets)
# print(f"Les couleurs après traitement {liste_couleurs(trajets)}")

#Exercice 3
# carte = creer_carte("Bretagne")
# tracer_point(carte,-1.6742900,48.1119800,"Rennes","blue")
# tracer_point(carte, -2.025674, 48.649337, "Saint-Malo","yellow")
# tracer_point(carte,  -1.553621, 47.218371, "Nantes","green")
# tracer_ligne(carte, [-1.553621,-1.6742900,-2.025674],[47.218371,48.1119800,48.649337],"Nantes - Rennes - Saint-Malo","#FF5533")
# afficher_carte(carte)

#Exercice 4
carte_tous_points_2d(trajets)

#Exercice 5

# coords = trajets[0]['Shape']
# print(type(coords))
# <class 'str'>
#Au chargement, le type est une chaine de caractères.


for trajet in trajets :
    trajet = prepare_lst_coord(trajet)
carte_toutes_lignes(trajets)