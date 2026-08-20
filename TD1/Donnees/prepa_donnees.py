import json
import os
import datetime

os.chdir("TD3/Donnees")

nom_fichier = "eco-counter-data_avril2024.json"

with open(nom_fichier, "r", encoding="utf-8") as fp:
    dico = json.load(fp)

fin = []
for rec in dico:
    rec2={}
    rec2["counter_id"]=rec["counter"]
    rec2["counts"]=rec["counts"]
    if rec2["counts"] == None : 
        rec2["counts"] = 0
    date = rec["date"]
    # print(date)
    rec2["date"]={"year":int(date[0:4]),"month":int(date[5:7]),"day":int(date[8:10]),"hour":int(date[11:13])}
    rec2["name"]=rec['name']
    rec2["gps_coord"]=[rec['geo']['lon'],rec['geo']['lat']]

    fin.append(rec2)

print(fin[0])

with open("eco-counter-data_clean.json", "w", encoding="utf-8") as fp :
    json.dump(fin,fp,indent=4)