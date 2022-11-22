import tweepy
import json
import csv
import os

#################### Définition des fonctions ###########################
#Q 1.2
def client_twitter(fichier):
    filecle=json.load(open(fichier))["twitter"]
    API_KEY = filecle["CONSUMER_KEY"]
    API_SECRET = filecle["CONSUMER_SECRET"]
    ACCESS_TOKEN  = filecle["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = filecle["ACCESS_TOKEN_SECRET"]

    client = tweepy.Client(consumer_key=API_KEY,
                        consumer_secret=API_SECRET,
                        access_token=ACCESS_TOKEN,
                        access_token_secret=ACCESS_TOKEN_SECRET)


    return client

 
def user_timeline (client,user_id):
    tweets = client.get_users_tweets(id=user_id, tweet_fields=['author_id','created_at','geo'],user_auth=True)
    for tweet in tweets.data:
          print(f"{tweet.id} : {tweet.text} (auteur :{tweet.author_id}, le {tweet.created_at})")

def recent_query(client,query,nb):
    tweets = client.search_recent_tweets(query=query, 
                                    tweet_fields=['author_id', 'created_at'],
                                     max_results=nb,user_auth=True)
    for tweet in tweets.data:
          print(f"{tweet.id} : {tweet.text} (auteur :{tweet.author_id}, le {tweet.created_at})")

#################### Tests et programme principal ###########################
#Création du client
client= client_twitter("TD9/corrige/credentials.json")

#Création d'un tewwet
response = client.create_tweet(text="Je crée un tweet avec le client API")

#Récupération d'un utilisateur
user = client.get_user(username="chris_suspecte",user_auth=True)
print(f"User : {user.data.name},identifiant : {user.data.id}, ")
id = user.data.id

#Affichage de la timeline de l'utilisateur
print("-------------------------")
print("Affichage de la timeline")
print("-------------------------")
user_timeline(client,id)


# Récupération de tweets avec une requete, on enlève les retweet
print("-------------------------")
print("Affichage de la requete des tweets récents")
print("-------------------------")
query = 'from:EmmanuelMacron -is:retweet'
recent_query(client,query,10)