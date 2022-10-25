import tweepy
import json
import csv
import os

#################### Définition des fonctions ###########################
#Q 1.2
def acces_api(fichier):

    filecle=json.load(open(fichier))["twitter"]
    consumer_key = filecle["CONSUMER_KEY"]
    consumer_secret = filecle["CONSUMER_SECRET"]
    key = filecle["ACCES"]
    secret = filecle["ACCES_SECRET"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    acces_api = tweepy.API(auth)

    return acces_api

#Question 2.1
def derniers_tweets(acces_api):
    return acces_api.user_timeline(count=2)

#Question 2.2
def texte_tweet(tweet):
    return tweet.text

#Question 2.3
def liste_textes_tweets(liste):
    l = []
    for tw in liste:
        l.append(texte_tweet(tw))
    return l

#Question 2.4
def auteur(tweet):
    return tweet.author.id, tweet.author.name


#Question 8 et 9
def tweeter_fichier(acces_api, fichier):
    tweets=[]
    for ligne in csv.DictReader(open(fichier, "r", encoding='utf-8'), delimiter=";"):
        message = ligne["text"]+" [Ceci est un faux tweet avec localisation]"
        latitude = float(ligne["lat"])
        longitude = float(ligne["lng"])
        mon_tweet=acces_api.update_status(message, lat=latitude,long=longitude)
        tweets.append(mon_tweet)
    return tweets

#question 10
def efface_tweets(acces_api,liste_ident):
    for id in liste_ident :
        acces_api.destroy_status(id)

#################### Tests et programma principal ###########################

os.chdir("TD9/corrige/")
#Q1.2
acces_api = acces_api("credentials.json")

#Q2.1
deux_tweets = derniers_tweets(acces_api)
# print(deux_tweets)
print(len(deux_tweets))

#Q2.2 et 2.3
print(liste_textes_tweets(deux_tweets))
# #['Super cours avec les L2 !!', 'En train de finaliser la préparation du CM']

# Q2.4
print("Test de la fonction auteur")
print(auteur(deux_tweets[0]))

# #test question 8
# chemin = os.path.join("data","tweets.csv")
# nouveau_tweets=tweeter_fichier(acces_api,chemin)

# #test question 9
# liste_id = [tweet.id for tweet in nouveau_tweets[0:2]]
# efface_tweets(acces_api,liste_id)
