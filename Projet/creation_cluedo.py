import json
import tweepy
import os


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




os.chdir("Projet")