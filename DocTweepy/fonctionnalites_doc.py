import tweepy
import json
import csv
import os

#################### Test de fonctionnalités ###########################
#Création d'un client Twitter
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

 #Récupérer la timeline d'un utilsateur
def user_timeline (client,user_id):
    tweets = client.get_users_tweets(id=user_id, tweet_fields=['author_id','created_at','geo'],user_auth=True)
    for tweet in tweets.data:
          print(f"{tweet.id} : {tweet.text} (auteur :{tweet.author_id}, le {tweet.created_at})")

#Récuperer les tweets récents d'une requete
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
# response = client.create_tweet(text="Je crée un tweet avec le client API")

#Récupération d'un utilisateur
# user = client.get_user(username="chris_suspecte",user_auth=True)
# print(f"User : {user.data.name},identifiant : {user.data.id}, ")
# id = user.data.id

#Affichage de la timeline de l'utilisateur
# print("-------------------------")
# print("Affichage de la timeline")
# print("-------------------------")
# user_timeline(client,id)


# Récupération de tweets avec une requete, on enlève les retweet
# print("-------------------------")
# print("Affichage de la requete des tweets récents")
# print("-------------------------")
# query = 'from:EmmanuelMacron -is:retweet'
# recent_query(client,query,10)

#Suppression d'un tweet : 
# idt = 1595063900797640709
# client.delete_tweet(idt)

# print("-------------------------")
# print("Affichage de la timeline")
# print("-------------------------")
# user_timeline(client,id)

#Consultation de tweets récents
# response = client.search_recent_tweets("Rennes",tweet_fields=["created_at","lang","author_id"],user_auth=True)
# tweets = response.data
# for tweet in tweets:
#     print("___________________________________________")
#     print(f"{tweet.id} (le {tweet.created_at}, en {tweet.lang} par {tweet.author_id}) : {tweet.text}") 

#Informations utilisateurs
# user = client.get_user(username="metropolerennes",user_auth=True,user_fields=["username"])
# print(f"Utilisateur : {user.data.name}, identifiant : {user.data.id}, ")

# user = client.get_user(id="16824660",user_auth=True,user_fields=["username","location"])
# print(f"Utilisateur : {user.data.name}, username :{user.data.username}, identifiant : {user.data.id}, lieu : {user.data.location}")

# response = client.get_users_followers(
#     "16824660", user_fields=["profile_image_url"],user_auth=True)

# for user in response.data:
#     print(user.username, user.profile_image_url)

# tweet_ids = [1460323737035677698, 1293593516040269825, 1293595870563381249]
# response = client.get_tweets(tweet_ids, tweet_fields=["created_at"],user_auth=True)
# for tweet in response.data:
#     print(tweet.text, tweet.created_at)

# user_id = 2244994945
# response = client.get_users_mentions(user_id,user_auth=True)
# for tweet in response.data:
#     print(tweet.id)
#     print(tweet.text)

# tweet_id = 1595360922314608641
# response = client.get_liking_users(tweet_id,user_auth=True)
# for user in response.data:
#     print(user.name)

tweet_id = 1595360922314608641
response = client.get_retweeters(tweet_id,user_auth=True)
for user in response.data:
    print(user.name)