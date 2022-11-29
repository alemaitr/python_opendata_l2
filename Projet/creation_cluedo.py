import json
import tweepy
import os

from cartographie import *


def acces_api(fichier, qui):

    filecle=json.load(open(fichier))[qui]
    consumer_key = filecle["CONSUMER_KEY"]
    consumer_secret = filecle["CONSUMER_SECRET"]
    key = filecle["ACCESS_TOKEN"]
    secret = filecle["ACCESS_TOKEN_SECRET"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    acces_api = tweepy.API(auth)

    return acces_api


def ecrire_tweet_loc(acces_api,  message,lieu):
    latitude = float(lieu["lat"])
    longitude = float(lieu["lng"])
    acces_api.update_status(message, lat=latitude,long=longitude)


def ecrire_tweet_non_loc(acces_api,  message):
    acces_api.update_status(message)

def coord_lieu(fichier, lieu):
    content  = json.load(open(fichier,encoding="utf-8"))
    coord = content[lieu]
    return coord

def tweet_suspect(qui, message, lieu = None):
    #Creer l'accès api
    api = acces_api("credentials.json",qui)

    if lieu != None : 
        coord = coord_lieu("places.json",lieu)
        ecrire_tweet_loc(api, message, coord)
    else :
        ecrire_tweet_non_loc(api,message)

def efface_tweet(qui, ident):
    api = acces_api("credentials.json",qui)
    api.destroy_status(ident)


def verifie_lieux(fichier):
    carte = creer_carte("Lieux Cluedo")
    content  = json.load(open(fichier,encoding="utf-8"))
    for lieu,coords in content.items() :
        tracer_point(carte, coords['lng'],coords['lat'],lieu)

    afficher_carte(carte)

os.chdir("Projet")

# verifie_lieux("places.json")

# efface_tweet("suspect_georges",1596842707640524802)

#####################################
############ Déjà tweeté ############
#Tweet la veille
# tweet_suspect("suspect_christiane","C'est vraiment un paysage magnifique","Brocéliande")
# tweet_suspect("suspect_jeanmi","Mon appartement ne ressemble à rien, il faut vraiment que j'aille chez Ikéa demain !","GastonBerger")
# tweet_suspect("suspect_georges","En pleines révisions, grosse journée de cours demain !")
# tweet_suspect("suspect_robert","Quelqu'un saurait où on peut acheter des tickets de métro parisien à Rennes ?","Sainte-Anne")
# tweet_suspect("suspect_christiane","Fin du week-end... départ pour la fac","République")

# #13h
# tweet_suspect("suspect_georges","Déjeuner avec les potes, Miam le RU de Villejean :-(","RU-Villejean")
# tweet_suspect("suspect_robert","Un sandwich vite fait en gare de Rennes, avant de monter dans le TGV pour Paris","Gare")
# tweet_suspect("suspect_christiane","Que de monde au Métronome ce midi !!","RU-Villejean")
# tweet_suspect("suspect_jeanmi","Ma liste de courses est prête, allée 18 place 12... Ikea, j'arrive !","GastonBerger")

# #14h45
# tweet_suspect("suspect_jeanmi","Au rayon cuisine, je trouve un magnifique couteau de boucher !!","IKEA-Rennes")
# tweet_suspect("suspect_christiane","Merci la BU Rennes 2, collecté plein d'infos sur l'Abbaye du Mt St Michel. Allons voir en vrai maintenant !","BU")
# tweet_suspect("suspect_georges","Mais que ce cours est long est pénible... ")

# #14h58
# tweet_suspect("suspect_jeanmi","Ouf, je sors d'Ikéa, bien chargé !!","IKEA-Rennes")
# tweet_suspect("suspect_georges","L'étudiante derrière moi pourrait elle arrêter de me tousser dessus ?")

# #15h06
# tweet_suspect("suspect_robert","Cool, mon train est à l'heure !! Bien arrivé à Montparnasse")

# # 15h25
# tweet_suspect("suspect_robert","Les ascenseurs de la Tour Eiffel sont en panne... ça va être sportif !!")
# tweet_suspect("suspect_jeanmi","Tout est déchargé, je m'attaque au montage des Billy !","GastonBerger")
# tweet_suspect("suspect_georges","Bon, ben y'a du boulot pour les partiels...")

# # 15h40
# tweet_suspect("suspect_christiane","Ouh là là, c'est le bazar le parking du Mont Saint Michel !","Pk-Mt-St-Michel")



# # 16h10
# tweet_suspect("suspect_robert","Paris pluvieux, mais Paris heureux !!")
# tweet_suspect("suspect_christiane","Magnifique visite de l'abbaye !!","Abbaye-Mt-St-Michel")
#####################################
############ A tweeter  #############





#21h 
tweet_suspect("suspect_robert","Retour à Rennes après cette escapade parisienne","Gare")
tweet_suspect("suspect_jeanmi","J'ai vaincu le montage ! fier de mon appartement témoin Ikéa ! Et le couteau tranche parfaitement !","GastonBerger")

