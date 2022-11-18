from datetime import datetime, timezone,timedelta
from pprint import pprint
import requests
from pytz import timezone

# Q 2.1 Tous les passages

def tous_passages_metro():
    url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-circulation-passages-tr&q=&rows=100&facet=nomcourtligne&facet=sens&facet=destination&facet=nomarret&facet=precision&refine.precision=Temps+r%C3%A9el&timezone=Europe%2FParis"
    contenu = requests.get(url)
    dico = contenu.json()
    liste_passage = []
    for metro in dico["records"] :
        if "depart" in metro["fields"].keys() :
            passage = {}
            passage["depart"] = datetime.fromisoformat(metro["fields"]["depart"])
            passage["destination"] = metro["fields"]["destination"]
            passage["nomarret"] = metro["fields"]["nomarret"]
            passage["ligne"]= metro["fields"]["nomcourtligne"]
            liste_passage.append(passage)
    return liste_passage

#Q2.2 Passages à venir
def a_venir(t, lespassages):
    passages_avenir = []

    for passage in lespassages :
        heuremetro = passage["depart"]
        maintenant = datetime.now(timezone("Europe/Paris"))
        if maintenant + timedelta(minutes=t)  > heuremetro and heuremetro> maintenant:
            passages_avenir.append(passage)

    return passages_avenir

#Q3.1 Passages dans une station
def passages_station(station):
    url = f"https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-circulation-passages-tr&q=&rows=100&facet=nomcourtligne&facet=sens&facet=destination&facet=nomarret&facet=precision&refine.nomarret={station}&precision=Temps+r%C3%A9el&timezone=Europe%2FParis"
    contenu = requests.get(url)
    dico = contenu.json()
    liste_passage = []
    for metro in dico["records"] :
        if "depart" in metro["fields"].keys() :
            passage = {}
            passage["depart"] = datetime.fromisoformat(metro["fields"]["depart"])
            passage["destination"] = metro["fields"]["destination"]
            # passage["nomarret"] = metro["fields"]["nomarret"]
            passage["ligne"]= metro["fields"]["nomcourtligne"]
            liste_passage.append(passage)
    return liste_passage

#Q3.3 Prochains passages dans une station

def prochain_passage_station(lespassages):
    dico={}
    # Parcours de tous les passages
    for passage in lespassages :
        cle=(passage["ligne"],passage["destination"])
        horaire = passage["depart"]
        maintenant = datetime.now(timezone("Europe/Paris"))
        if horaire > maintenant:
            if cle in dico.keys() :
                if dico[cle]>horaire :
                    dico[cle]=horaire
            else:
                dico[cle]=horaire

    return dico

def affichage_station(station):
    passages = passages_station(station)
    prochains = prochain_passage_station(passages)
    print("********************************************")
    print(f"Bienvenue à la station {station}")
    for cle,heure in prochains.items():
        heureformat = heure.strftime("%H:%M:%S")
        print(f"Ligne {cle[0]}, direction {cle[1]} : métro à {heureformat}")
    print("********************************************")
# # Q 1.7 Récupération des passages de métro
# passages_brut = requests.get("https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-circulation-passages-tr&q=&rows=100&facet=nomcourtligne&facet=sens&facet=destination&facet=nomarret&facet=precision&refine.precision=Temps+r%C3%A9el&timezone=Europe%2FParis")
# passages = passages_brut.json()

# # Q 1.8 Nombre de passages
# print(f"Nombre de passages annoncés : {passages['nhits']}")
# print(f"Nombre de passages comptés : {len(passages['records'])}")
# print("Note : différence normale puisque notre requête renvoie les 100 prochains passages")

#Test fonctions exercice 2
passages = tous_passages_metro()
#pprint(passages)
print(len(passages))
avenir = a_venir(10,passages)
# pprint(avenir)
print(len(avenir)," passages dans les 10 prochaines minutes")

#Tests exercice 3
pass_gare = passages_station("Gares")
# pprint(pass_gare)
procgare = prochain_passage_station(pass_gare)
pprint(procgare)
affichage_station("Gares")