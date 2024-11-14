from datetime import datetime, timezone,timedelta
from pprint import pprint
import requests
from pytz import timezone

# Q 2.1 Tous les passages

def extrait_infos_passages(lst_brute):
    liste_passage = []
    for metro in lst_brute :
        if "depart" in metro.keys() and metro["depart"]: #Sous entendu not None
            if "arrivee" in metro.keys() and metro["arrivee"]: #Sous entendu not None
                passage = {}
                passage["depart"] = datetime.fromisoformat(metro["depart"])
                format_arrivee ="%Y-%m-%d %H:%M:%S%z"
                passage["arrivee"] = datetime.strptime(metro["arrivee"],format_arrivee)
                # print(metro["arrivee"], "----->", passage["arrivee"])
                passage["destination"] = metro["destination"]
                passage["nomarret"] = metro["nomarret"]
                passage["ligne"]= metro["nomcourtligne"]                
                liste_passage.append(passage)
    return liste_passage

# #Q2.2 durée moyenne

def duree_moyenne(lst_passages):
    duree_cumulee = timedelta(0)
    for passage in lst_passages:
        duree = passage["depart"]-passage["arrivee"]
        duree_cumulee+=duree
    return duree_cumulee/len(lst_passages)

# def a_venir(t, lespassages):
#     passages_avenir = []

#     for passage in lespassages :
#         heuremetro = passage["depart"]
#         maintenant = datetime.now(timezone("Europe/Paris"))
#         if maintenant + timedelta(minutes=t)  > heuremetro and heuremetro> maintenant:
#             passages_avenir.append(passage)

#     return passages_avenir

#Q3.1 Passages dans une station
def passages_station(station, les_passages):
    return [passage for passage in les_passages if passage['nomarret']==station]

#Q3.3 Prochains passages dans une station

def prochain_passage_station(lespassages):
    dico={}
    # Parcours de tous les passages
    for passage in lespassages :
        cle=(passage["ligne"],passage["destination"])
        horaire = passage["depart"]
        maintenant = datetime.now(timezone("Europe/Paris"))
        if horaire > maintenant: #On vérifie que l'horaire de départ n'est pas encore passé
            if cle in dico.keys() :
                if horaire < dico[cle]: #Si on a trouvé un horaire avant le précédent
                    dico[cle]=horaire
            else:
                dico[cle]=horaire

    return dico

def affichage_station(station,lstpassages):
    passages = passages_station(station,lstpassages)
    prochains = prochain_passage_station(passages)
    print("********************************************")
    print(f"Bienvenue à la station {station}")
    print("********************************************")
    for cle,heure in prochains.items():

        heureformat = heure.astimezone(timezone("Europe/Paris")).strftime("%H:%M:%S")
        print(f"Ligne {cle[0]}, direction {cle[1]} : prochain métro à {heureformat}")
    print("********************************************")

if __name__=="__main__":

    # Q 1.6 Récupération des passages de métro
    url = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-metro-circulation-passages-tr/records?limit=100&refine=precision%3A%22Temps%20r%C3%A9el%22"
    reponse = requests.get(url).json()
    # print(reponse)

    # Q 1.7 Nombre de passages
    print(f"Nombre de passages annoncés : {reponse['total_count']}")
    print(f"Nombre de passages comptés dans la première requête: {len(reponse['results'])}")
    print("Note : différence normale puisque notre requête renvoie seulement les 100 prochains passages")

    # Q 1.8 Liste des passages
    liste_passages_bruts = reponse["results"]
    # Q 1.9 Complément avec Offset de 100
    url2 = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-metro-circulation-passages-tr/records?offset=100&limit=100&refine=precision%3A%22Temps%20r%C3%A9el%22"
    reponse2 = requests.get(url2).json()
    print(f"Nombre de passages comptés dans la seconde requete : {len(reponse2['results'])}")
    liste_passages_bruts+=reponse2['results']
    print(f"Nombre de passages disponibles au final : {len(liste_passages_bruts)}")

    # Exercice 2
    liste_passages = extrait_infos_passages(liste_passages_bruts)
    # pprint(liste_passages)
    print(f"Nombre de passages apres filtrage arrivee/depart non vide : {len(liste_passages)}")

    moyenne = duree_moyenne(liste_passages)
    print(f"Temps moyen passé dans chaque station : {moyenne}")

    # Exercice 3
    # Q3.2
    pass_gare = passages_station("Gares",liste_passages)
    print("Prochains passages à la station Gares :")
    pprint(pass_gare)
    procgare = prochain_passage_station(pass_gare)
    # pprint(procgare)
    affichage_station("Gares",liste_passages)
    affichage_station("Saint-Germain",liste_passages)