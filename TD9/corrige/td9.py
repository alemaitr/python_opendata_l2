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

#Q2.1
def tweeter(client,message):
    response = client.create_tweet(text=message)
    return response.data["id"]

#Q3.1
def details_utilisateur(client, nom):
    user = client.get_user(username=nom,user_auth=True,user_fields=["created_at","description","location"])
    dico={}

    dico["Utilisateur"]=user.data.username
    dico["User_id"]=user.data.id
    dico["Nom"]=user.data.name
    dico["Lieu"]=user.data.location
    dico["Description"]=user.data.description
    dico["Date de création"]=user.data.created_at.strftime("%m/%Y")
    
    return dico

#################### Tests et programme principal ###########################

os.chdir("TD9/corrige/")
#Q1.2
client= client_twitter("credentials.json")

#Q2.2
# id = tweeter(client, "Je suis en TP de Python")

#Q3.1
dico = details_utilisateur(client,"UnivRennes_2")
print(dico)

#Q3.2
mon_ident = details_utilisateur(client,"chris_suspecte")["User_id"]
print(f"Mon identifiant : {mon_ident}")