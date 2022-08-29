import csv
import os
import sys
import json
import graphh


#######################################################################
#Définition des fonctions
#######################################################################
def acces_cle_api():
    fp = open("credentials.json", "r", encoding="utf-8")
    data = json.load(fp)
    return data["GraphHopper"]
    
#Fonctions pour l'exercice 4

#Fonctions pour l'exercice 5






#######################################################################
#Tests et appels de fonctions
#######################################################################
os.chdir("TD2")

#Exercice 1
macle = acces_cle_api()
print(f"Ma clé d'API : {macle}")

#Exercice 2
gh_client = graphh.GraphHopper(api_key=macle)

coor_beaulieu = gh_client.address_to_latlong("Rennes Beaulieu")
coor_villejean = gh_client.address_to_latlong("Rennes Beaulieu")

print(coor_beaulieu)

#Exercice 3


#Exercice 4


#Exercice 5
