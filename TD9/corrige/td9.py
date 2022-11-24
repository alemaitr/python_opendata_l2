import tweepy
import json
import os
from pprint import pprint
import datetime
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

#Q2.3
def efface_tweet(client,id_tweet):
    client.delete_tweet(id_tweet)

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
#Q4.1 et 4.3
def derniers_tweets(client,user_id,nb):
    response = client.get_users_tweets(user_id,user_auth=True,max_results=nb,tweet_fields=["created_at","geo"])
    lst = []
    for tweet in response.data :
        dico = {}
        dico["tweet_id"] = tweet.id
        dico["texte"] = tweet.text
        dico["date"] = tweet.created_at
        if tweet.geo != None : 
            print(tweet.geo)       
            if 'coordinates' in tweet.geo.keys():
                coords = tweet.geo['coordinates']['coordinates']
                dico["long"] = coords[0]
                dico["lat"] = coords[1]
        lst.append(dico)
    return lst

#Q5.1

def tweet_favoris(client,user):
    nb = 50

    #On a besoin pour cela de l'id du user
    details = details_utilisateur(client,user)
    user_id = details['User_id']
    user_nom = details['Nom']
    print(user_id)

    #On reque les nb derniers tweets, avec le nb de like 
    response = client.get_users_tweets(user_id,user_auth=True,max_results=nb,tweet_fields=["created_at","public_metrics"])
    nbmax = 0
    t_like = None    
    for tweet in response.data :
        like =tweet.public_metrics['like_count'] 
        if like>nbmax :
            t_like = tweet

    date = t_like.created_at.strftime("%d/%m/%y à %H:%M")
    print(f'Le tweet de {user_nom} ayant récolté le plus de like date du {date} : \n {"-"*20} \n {t_like.text}\n {"-"*20}' )


#Q5.2 
def repartition_mois(client,user,mois):
    user_id = details_utilisateur(client,user)['User_id']
    debut = datetime.datetime(day=1,month=mois,year=2022)
    fin = datetime.datetime(day=1,month=mois+1,year=2022)
    response = client.get_users_tweets(user_id,user_auth=True,start_time=debut,end_time=fin,max_results=100,tweet_fields=["created_at"])
    
    dicojour = {i:0 for i in range(1,30)}
    for tweet in response.data:
        jour = tweet.created_at.day
        dicojour[jour]=dicojour.get(jour,0)+1

    return dicojour

#Q5.3
def followers_communs(client, user1, user2):
    #On a besoin pour cela de l'id du user
    user_id1 = details_utilisateur(client,user1)['User_id']
    user_id2 = details_utilisateur(client,user2)['User_id']


    follow1= client.get_users_followers(id=user_id1,user_auth=True,max_results=1000)
    
    lst1 = []#Les followers du premier
    for user in follow1.data :
        lst1.append(user.id)
    print("Nombre de followers de ",user1,len(lst1))

    follow2= client.get_users_followers(id=user_id2,user_auth=True,max_results=1000)
    lstnoms = []
    print("Nombre de followers de",user2,len(follow2.data))
    for user in follow2.data :
        if user.id in lst1:
            lstnoms.append(user.name)
    return lstnoms


#################### Tests et programme principal ###########################

os.chdir("TD9/corrige/")
#Q1.2
client= client_twitter("credentials.json")

#Q2.2
# id = tweeter(client, "Je suis en TP de Python")

#Q2.3
# client.delete_tweet(1595683728202039297)
#Q3.1
# dico = details_utilisateur(client,"UnivRennes_2")
# print(dico)

#Q3.2
# mon_ident = details_utilisateur(client,"chris_suspecte")["User_id"]
# print(f"Mon identifiant : {mon_ident}")

#Q4.1
# dico = derniers_tweets(client,mon_ident,5)
# pprint(dico)

#Q4.4
# ident_test = details_utilisateur(client,"chris_suspecte")["User_id"]
# dico = derniers_tweets(client,ident_test,5)
# pprint(dico)

#Q5.1
# tweet_favoris(client,"UnivRennes_2")

#Q5.2
# dico = repartition_mois(client,"UnivRennes_2",9)
# print(f"Voici la répartition des tweets de Rennes 2 sur le mois de septembre 2022")
# print(dico)
#Q5.3
# lst_comm = followers_communs(client,"UnivRennes_2","metropolerennes")
# print(f"Voici le nom de {len(lst_comm)} followers communs à Université Rennes 2 et Rennes métropole\n Il s'agit de : \n {lst_comm}")
