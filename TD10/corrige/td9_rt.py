import tweepy
import json
from pprint import pprint
import datetime


def client_twitter(fname):
    json_content = json.load(open(fname, "r"))
    return tweepy.Client(consumer_key=json_content["twitter"]["CONSUMER_KEY"],
                         consumer_secret=json_content["twitter"]["CONSUMER_SECRET"],
                         access_token=json_content["twitter"]["ACCESS_TOKEN"],
                         access_token_secret=json_content["twitter"]["ACCESS_TOKEN_SECRET"])

def tweeter(client, message):
    return client.create_tweet(text=message).data["id"]

def efface_tweet(client, tweet_id):
    client.delete_tweet(tweet_id)

def details_utilisateur(client, nom_utilisateur):
    user_data = client.get_user(username=nom_utilisateur, 
                                user_auth=True,
                                user_fields=["username", "location", "description", "created_at"])
    return {
        "Utilisateur": user_data.data.username,
        "Nom": user_data.data.name,
        "User_id": user_data.data.id,
        "Description": user_data.data.description,
        "Lieu": user_data.data.location,
        "Date de création": user_data.data.created_at.strftime("%m/%Y")
    }

def derniers_tweets(client, twitter_id, n):
    tweets = client.get_users_tweets(twitter_id, 
                                     tweet_fields=["created_at", "text", "id", "geo"],
                                     max_results=n,
                                     user_auth=True)
    l_tweets = []
    for tw in tweets.data:
        if tw.geo is None or "coordinates" not in tw.geo.keys():
            l_tweets.append({
                "date": tw.created_at,
                "texte": tw.text,
                "tweet_id": tw.id
            })
        else:
            l_tweets.append({
                "date": tw.created_at,
                "texte": tw.text,
                "tweet_id": tw.id,
                "long": tw.geo["coordinates"]["coordinates"][0],
                "lat": tw.geo["coordinates"]["coordinates"][1]
            })
    return l_tweets

def print_most_liked_tweet(client, username, n=50):
    details = details_utilisateur(client, username)
    user_id = details["User_id"]
    name = details["Nom"]
    tweets = client.get_users_tweets(user_id, 
                                     tweet_fields=["created_at", "text", "public_metrics"],
                                     max_results=n,
                                     user_auth=True)
    most_liked_tweet = None
    max_likes = -1
    for tw in tweets.data:
        n_likes = tw.public_metrics.get("like_count", 0)
        if n_likes > max_likes:
            most_liked_tweet = tw
    print(f"Le tweet de {name} ayant récolté le plus de like date du {most_liked_tweet.created_at.strftime('%d/%m/%Y à %H:%M')} :")
    print("------")
    print(most_liked_tweet.text)
    print("------")

def repartition_mois(client, user, mois, annee):
    user_id = details_utilisateur(client, user)['User_id']
    debut = datetime.datetime(day=1, month=mois, year=annee)
    fin = datetime.datetime(day=1, month=mois+1, year=annee)
    response = client.get_users_tweets(user_id, user_auth=True, start_time=debut, end_time=fin, max_results=100, tweet_fields=["created_at"])
    
    dicojour = {}
    for tweet in response.data:
        jour = tweet.created_at.day
        dicojour[jour]=dicojour.get(jour, 0) + 1

    return dicojour
        
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

client = client_twitter("credentials.json")
# print(client)

# tid = tweeter(client, "Je suis en TP Python (2ème fois)")
# efface_tweet(client, tid)

pprint(details_utilisateur(client, "UnivRennes_2"))
my_id = details_utilisateur(client, "tavenard_py")["User_id"]
pprint(derniers_tweets(client, my_id, n=10))

chris_id = details_utilisateur(client, "chris_suspecte")["User_id"]
pprint(derniers_tweets(client, chris_id, n=10))

print_most_liked_tweet(client, "UnivRennes_2")
print(repartition_mois(client, "UnivRennes_2", 9, 2022))

print(followers_communs(client, "UnivRennes_2", "metropolerennes"))